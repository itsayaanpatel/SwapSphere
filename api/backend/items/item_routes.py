from flask import Blueprint, request, jsonify, make_response, current_app
from models import db, Item

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

from backend.db_connection import db

items = Blueprint('items', __name__)

# Add a new item
@items.route('/items', methods=['POST'])
def add_item():
    data = request.json
    
    cursor = db.get_db().cursor()
    cursor.execute('''
        INSERT INTO Items (user_id, title, description, category, estimated_value)
        VALUES (%s, %s, %s, %s, %s)
    ''', (data['user_id'], data['title'], data['description'], 
          data['category'], data['estimated_value']))
    
    db.get_db().commit()
    return make_response(jsonify({'message': 'Item added!'}), 201)

# Get a user's items
@items.route('/items/user/<user_id>', methods=['GET'])
def get_user_items(user_id):
    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT * FROM Items WHERE user_id = %s
    ''', (user_id,))
    
    items = cursor.fetchall()
    return make_response(jsonify(items), 200)

# Update an item
@items.route('/items/<item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.json
    
    cursor = db.get_db().cursor()
    cursor.execute('''
        UPDATE Items 
        SET title = %s, description = %s, category = %s, estimated_value = %s
        WHERE item_id = %s
    ''', (data['title'], data['description'], data['category'], 
          data['estimated_value'], item_id))
    
    db.get_db().commit()
    return make_response(jsonify({'message': 'Item updated!'}), 200)

# Delete an item
@items.route('/items/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM Items WHERE item_id = %s', (item_id,))
    db.get_db().commit()
    
    return make_response(jsonify({'message': 'Item deleted!'}), 200)

# Get item categories
@items.route('/categories', methods=['GET'])
def get_categories():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT DISTINCT category FROM Items WHERE category IS NOT NULL')
    
    categories = [row['category'] for row in cursor.fetchall()]
    return make_response(jsonify(categories), 200)