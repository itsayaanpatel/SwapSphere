from flask import Blueprint, jsonify
from api.models import db, Item

items_bp = Blueprint('items', __name__)

@items_bp.route('/items', methods=['GET'])
def get_items():
    """Implementation for [Jake-1], [Emma-1]"""
    try:
        items = Item.query.all()
        return jsonify([{
            'id': item.id,
            'title': item.title,
            'category': item.category,
            'estimated_value': item.estimated_value
        } for item in items]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
