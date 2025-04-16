"""
seller_routes.py

endpoints:

1. GET /seller/items:
   Retrieves all items listed by a seller. Expects a query parameter "seller_id" which
   corresponds to the user_id in the Users table.

2. GET /seller/trade_history:
   Retrieves the trade history for items offered by the seller. This endpoint joins the
   Trades, Trade_Items, and Items tables to return trade details for items offered by the seller.

3. POST /seller/items:
   Adds (uploads) a new item to the seller’s inventory. The required fields are seller_id,
   title, description, category, and estimated_value. The status is set to 'Available' by default.

4. PUT /seller/items/<item_id>:
   Updates the details for an existing item in the seller's inventory. Accepts updated
   values for title, description, category, estimated_value, and optionally status.

5. DELETE /seller/items/<item_id>:
   Deletes an item from the seller's inventory.

This blueprint is registered with the URL prefix "/seller". For instance, GET /seller/items
will return the items for the specified seller.

MORE Notes:
    - The database schema uses: Users, Items, Trades, Trade_Items, etc.
    - Sample data has been seeded by the provided SQL statements.
    - The implementation uses one GET route for items, one GET route for trade history,
      one POST route for adding an item, one PUT route for updating an item, and one DELETE
      route for removing an item.
"""

from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

# Create the Blueprint for seller routes.
seller = Blueprint('seller', __name__)

@seller.route('/items', methods=['GET'])
def get_seller_items():
    """
    GET /seller/items

    Retrieves all items listed by the seller.
    Expects a query parameter 'seller_id' (which corresponds to the user_id in the Users table).

    Returns:
        A JSON response containing a list of items with the following fields:
            - item_id
            - title
            - description
            - category
            - estimated_value
            - status
            - created_at
    """
    seller_id = request.args.get('seller_id')
    if not seller_id:
        return make_response(jsonify({"error": "seller_id query parameter is required"}), 400)
    
    query = """
        SELECT item_id, title, description, category, estimated_value, status, created_at
        FROM Items
        WHERE user_id = %s
    """
    cursor = db.get_db().cursor()
    cursor.execute(query, (seller_id,))
    items = cursor.fetchall()
    
    return make_response(jsonify(items), 200)

@seller.route('/trade_history', methods=['GET'])
def get_trade_history():
    """
    GET /seller/trade_history

    Retrieves the trade history for items offered by the seller.
    Expects a query parameter 'seller_id' (which is used as the offered_by field in Trade_Items).

    Returns:
        A JSON response containing a list of trades with the following fields:
            - trade_id
            - item_id
            - title (from the Items table)
            - status (from the Trades table)
            - cash_adjustment (from the Trades table)
            - created_at (from the Trades table)
    """
    seller_id = request.args.get('seller_id')
    if not seller_id:
        return make_response(jsonify({"error": "seller_id query parameter is required"}), 400)
    
    query = """
        SELECT t.trade_id, i.item_id, i.title, t.status, t.cash_adjustment, t.created_at
        FROM Trades t
        JOIN Trade_Items ti ON t.trade_id = ti.trade_id
        JOIN Items i ON ti.item_id = i.item_id
        WHERE ti.offered_by = %s
        ORDER BY t.created_at DESC
    """
    cursor = db.get_db().cursor()
    cursor.execute(query, (seller_id,))
    trade_history = cursor.fetchall()
    
    return make_response(jsonify(trade_history), 200)

@seller.route('/items', methods=['POST'])
def add_new_item():
    """
    POST /seller/items

    Adds a new item to the seller's inventory.
    Expects a JSON payload with the following fields:
        - seller_id: The ID of the seller (user_id from Users).
        - title: The title of the item.
        - description: A description of the item.
        - category: The category to which the item belongs.
        - estimated_value: The estimated value of the item.

    Returns:
        A JSON response confirming the item was added along with the new item_id.
    """
    data = request.json
    seller_id = data.get('seller_id')
    title = data.get('title')
    description = data.get('description')
    category = data.get('category')
    estimated_value = data.get('estimated_value')
    
    if not (seller_id and title and estimated_value and category):
        return make_response(jsonify({
            "error": "Missing required fields (seller_id, title, estimated_value, category)"
        }), 400)
    
    query = """
        INSERT INTO Items (user_id, title, description, category, estimated_value, status)
        VALUES (%s, %s, %s, %s, %s, 'Available')
    """
    cursor = db.get_db().cursor()
    cursor.execute(query, (seller_id, title, description, category, estimated_value))
    db.get_db().commit()
    new_item_id = cursor.lastrowid
    
    return make_response(jsonify({"message": "Item added successfully", "item_id": new_item_id}), 200)

    
@seller.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    """
    PUT /seller/items/<item_id>

    Updates the details of an existing item in the seller's inventory.
    Expects a JSON payload with fields to update, such as:
        - title
        - description
        - category
        - estimated_value
        - status (optional, e.g., 'Available', 'Traded', or 'Pending')

    Parameters:
        item_id (int): The ID of the item to update.

    Returns:
        A JSON response confirming that the item was updated successfully.
    """
    data = request.json
    title = data.get('title')
    description = data.get('description')
    category = data.get('category')
    estimated_value = data.get('estimated_value')
    status = data.get('status', 'Available')
    
    if not (title and description and estimated_value and category):
        return make_response(jsonify({"error": "Missing required fields for update"}), 400)
    
    query = """
        UPDATE Items
        SET title = %s, description = %s, category = %s, estimated_value = %s, status = %s
        WHERE item_id = %s
    """
    cursor = db.get_db().cursor()
    cursor.execute(query, (title, description, category, estimated_value, status, item_id))
    db.get_db().commit()
    
    return make_response(jsonify({"message": f"Item {item_id} updated successfully"}), 200)

@seller.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """
    DELETE /seller/items/<item_id>

    Deletes an item from the seller's inventory.
    
    Parameters:
        item_id (int): The ID of the item to delete.
    
    Returns:
        A JSON response confirming that the item has been removed.
    """
    query = "DELETE FROM Items WHERE item_id = %s"
    cursor = db.get_db().cursor()
    cursor.execute(query, (item_id,))
    db.get_db().commit()
    
    return make_response(jsonify({"message": f"Item {item_id} removed successfully"}), 200)