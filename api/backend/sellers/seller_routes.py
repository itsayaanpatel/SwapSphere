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