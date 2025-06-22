from flask import Blueprint, request, jsonify
from app.models.models import db, ShopItemCategory

category_bp = Blueprint('category_bp', __name__, url_prefix='/categories')

@category_bp.route('', methods=['POST'])
def create_category():
    data = request.get_json()
    if not data or not data.get('title'):
        return jsonify({'message': 'Missing title'}), 400

    if ShopItemCategory.query.filter_by(title=data['title']).first():
        return jsonify({'message': 'Category with this title already exists'}), 409

    new_category = ShopItemCategory(
        title=data['title'],
        description=data.get('description', '')
    )
    db.session.add(new_category)
    db.session.commit()
    return jsonify(new_category.to_dict()), 201

@category_bp.route('', methods=['GET'])
def get_categories():
    categories = ShopItemCategory.query.all()
    return jsonify([category.to_dict() for category in categories]), 200

@category_bp.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = ShopItemCategory.query.get(category_id)
    if not category:
        return jsonify({'message': 'Category not found'}), 404
    return jsonify(category.to_dict()), 200

@category_bp.route('/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    category = ShopItemCategory.query.get(category_id)
    if not category:
        return jsonify({'message': 'Category not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    if 'title' in data and data['title'] != category.title:
        if ShopItemCategory.query.filter_by(title=data['title']).first():
            return jsonify({'message': 'Another category with this title already exists'}), 409
        category.title = data['title']

    category.description = data.get('description', category.description)

    db.session.commit()
    return jsonify(category.to_dict()), 200

@category_bp.route('/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    category = ShopItemCategory.query.get(category_id)
    if not category:
        return jsonify({'message': 'Category not found'}), 404

    # Optional: Check if category is used by any ShopItem
    if category.shop_items:
         return jsonify({'message': 'Cannot delete category as it is associated with shop items. Remove associations first.'}), 409

    db.session.delete(category)
    db.session.commit()
    return jsonify({'message': 'Category deleted'}), 200
