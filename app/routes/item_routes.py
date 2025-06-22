from flask import Blueprint, request, jsonify
from app.models.models import db, ShopItem, ShopItemCategory

item_bp = Blueprint('item_bp', __name__, url_prefix='/items')

@item_bp.route('', methods=['POST'])
def create_item():
    data = request.get_json()
    if not data or not data.get('title') or data.get('price') is None:
        return jsonify({'message': 'Missing title or price'}), 400

    if ShopItem.query.filter_by(title=data['title']).first():
        return jsonify({'message': 'Item with this title already exists'}), 409

    new_item = ShopItem(
        title=data['title'],
        description=data.get('description', ''),
        price=data['price']
    )

    category_ids = data.get('category_ids', [])
    if category_ids:
        categories = ShopItemCategory.query.filter(ShopItemCategory.id.in_(category_ids)).all()
        if len(categories) != len(category_ids):
            return jsonify({'message': 'One or more categories not found'}), 404
        new_item.categories = categories

    db.session.add(new_item)
    db.session.commit()
    return jsonify(new_item.to_dict()), 201

@item_bp.route('', methods=['GET'])
def get_items():
    items = ShopItem.query.all()
    return jsonify([item.to_dict() for item in items]), 200

@item_bp.route('/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = ShopItem.query.get(item_id)
    if not item:
        return jsonify({'message': 'Item not found'}), 404
    return jsonify(item.to_dict()), 200

@item_bp.route('/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = ShopItem.query.get(item_id)
    if not item:
        return jsonify({'message': 'Item not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    if 'title' in data and data['title'] != item.title:
        if ShopItem.query.filter_by(title=data['title']).first():
            return jsonify({'message': 'Another item with this title already exists'}), 409
        item.title = data['title']

    item.description = data.get('description', item.description)
    item.price = data.get('price', item.price)

    if 'category_ids' in data:
        category_ids = data.get('category_ids', [])
        if not category_ids: # If empty list provided, clear categories
            item.categories = []
        else:
            categories = ShopItemCategory.query.filter(ShopItemCategory.id.in_(category_ids)).all()
            if len(categories) != len(set(category_ids)): # Use set to handle potential duplicates in input
                # Find which IDs were not found
                found_ids = {cat.id for cat in categories}
                not_found_ids = [cid for cid in category_ids if cid not in found_ids]
                return jsonify({'message': f'One or more categories not found: {not_found_ids}'}), 404
            item.categories = categories

    db.session.commit()
    return jsonify(item.to_dict()), 200

@item_bp.route('/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = ShopItem.query.get(item_id)
    if not item:
        return jsonify({'message': 'Item not found'}), 404

    # Optional: Check if item is part of any OrderItem
    if item.order_items:
        return jsonify({'message': 'Cannot delete item as it is part of existing orders. Remove from orders first or handle appropriately.'}), 409

    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item deleted'}), 200
