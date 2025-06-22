from flask import Blueprint, request, jsonify
from app.models.models import db, Order, OrderItem, Customer, ShopItem

order_bp = Blueprint('order_bp', __name__, url_prefix='/orders')

@order_bp.route('', methods=['POST'])
def create_order():
    data = request.get_json()
    if not data or not data.get('customer_id') or not data.get('items'):
        return jsonify({'message': 'Missing customer_id or items'}), 400

    customer = Customer.query.get(data['customer_id'])
    if not customer:
        return jsonify({'message': 'Customer not found'}), 404

    new_order = Order(customer_id=data['customer_id'])

    order_items_data = data.get('items', [])
    if not order_items_data:
        return jsonify({'message': 'Order must contain at least one item'}), 400

    for item_data in order_items_data:
        shop_item_id = item_data.get('shop_item_id')
        quantity = item_data.get('quantity')

        if not shop_item_id or quantity is None:
            return jsonify({'message': 'Each item must have shop_item_id and quantity'}), 400

        if not isinstance(quantity, int) or quantity <= 0:
            return jsonify({'message': f'Invalid quantity for item {shop_item_id}. Must be a positive integer.'}), 400


        shop_item = ShopItem.query.get(shop_item_id)
        if not shop_item:
            # Rollback potential partial adds if one item is not found
            # db.session.rollback() # Not strictly needed here as we haven't added the order yet
            return jsonify({'message': f'ShopItem with id {shop_item_id} not found'}), 404

        order_item = OrderItem(
            shop_item_id=shop_item_id,
            quantity=quantity
            # order_id will be set by relationship backref or when order is added to session with items
        )
        new_order.items.append(order_item)

    try:
        db.session.add(new_order)
        # OrderItems are cascaded due to relationship settings or need to be added explicitly if not.
        # The `cascade="all, delete-orphan"` on Order.items handles adding OrderItems.
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error creating order', 'error': str(e)}), 500

    return jsonify(new_order.to_dict()), 201

@order_bp.route('', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify([order.to_dict() for order in orders]), 200

@order_bp.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'message': 'Order not found'}), 404
    return jsonify(order.to_dict()), 200

@order_bp.route('/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'message': 'Order not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    # Update customer_id if provided
    if 'customer_id' in data:
        customer = Customer.query.get(data['customer_id'])
        if not customer:
            return jsonify({'message': 'New customer not found'}), 404
        order.customer_id = data['customer_id']

    # Update items: This is complex. Usually, you'd replace all items or provide methods to add/remove/update specific items.
    # For simplicity, this PUT will replace all items in the order.
    if 'items' in data:
        order_items_data = data.get('items', [])
        if not order_items_data: # If items list is empty, it means remove all items from order
            # order.items = [] # This works if cascade delete-orphan is set
            # Safer: iterate and delete
            for item in list(order.items): # Iterate over a copy for safe removal
                db.session.delete(item)
        else:
            # Remove existing items first
            for item in list(order.items):
                db.session.delete(item)
            db.session.flush() # Ensure deletes are processed before adds to avoid PK issues if items are re-added

            new_order_items = []
            for item_data in order_items_data:
                shop_item_id = item_data.get('shop_item_id')
                quantity = item_data.get('quantity')

                if not shop_item_id or quantity is None:
                    return jsonify({'message': 'Each item must have shop_item_id and quantity'}), 400

                if not isinstance(quantity, int) or quantity <= 0:
                    return jsonify({'message': f'Invalid quantity for item {shop_item_id}. Must be a positive integer.'}), 400

                shop_item = ShopItem.query.get(shop_item_id)
                if not shop_item:
                    # db.session.rollback() # Rollback changes if an item is not found
                    return jsonify({'message': f'ShopItem with id {shop_item_id} not found'}), 404

                order_item = OrderItem(
                    shop_item_id=shop_item_id,
                    quantity=quantity,
                    order_id=order.id # Explicitly set order_id
                )
                new_order_items.append(order_item)
            order.items = new_order_items # Assign the new list of items
            # db.session.add_all(new_order_items) # Add new items to session if not cascaded

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error updating order', 'error': str(e)}), 500

    return jsonify(order.to_dict()), 200

@order_bp.route('/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'message': 'Order not found'}), 404

    # OrderItems are deleted due to cascade="all, delete-orphan" on Order.items relationship
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Order deleted'}), 200
