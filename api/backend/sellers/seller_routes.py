"""
seller_routes.py

This module contains Flask routes for functionalities specific to the Seller persona
in the SwapSphere application. These endpoints enable sellers (like Emma) to manage their inventory,
view their trade history, and upload or modify their items. The available endpoints include:

1. GET /seller/items:
   Retrieves all items listed by the seller. Expects a query parameter 'seller_id' to filter items.

2. GET /seller/trade_history:
   Retrieves the trade history for a seller’s items. Expects a query parameter 'seller_id'.

3. POST /seller/items:
   Adds (uploads) a new item to the seller's inventory. Expects a JSON payload with item details.

4. PUT /seller/items/<item_id>:
   Updates the details for an existing item using the provided item_id. Expects a JSON payload with updated fields.

5. DELETE /seller/items/<item_id>:
   Deletes an item from the seller's inventory based on item_id.

This blueprint is registered with the URL prefix "/seller". For example, the GET endpoint for retrieving items
will be available at GET /seller/items.

Note:
    - The SQL queries assume that tables such as 'items' and 'trades' exist in your MySQL database.
    - Sample data may have been seeded via Mockaroo/Faker.
    - Each route includes appropriate HTTP methods and docstrings, following the REST API matrix and project rules.
"""

from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

# Create the Blueprint for seller routes.
seller = Blueprint('seller', __name__)

@seller.route('/items', methods=['GET'])
def get_seller_items():
    """
    GET /seller/items

    Retrieves all items listed by a seller.
    Expects a query parameter 'seller_id' to filter the items.

    Returns:
        A JSON response containing a list of items for the specified seller with fields such as:
            - id
            - item_name
            - description
            - estimated_value
            - category
            - image_url (if available)
    """
    seller_id = request.args.get('seller_id')
    if not seller_id:
        return make_response(jsonify({"error": "seller_id query parameter is required"}), 400)
    
    query = """
        SELECT id, item_name, description, estimated_value, category, image_url
        FROM items
        WHERE seller_id = %s
    """
    cursor = db.get_db().cursor()
    cursor.execute(query, (seller_id,))
    items = cursor.fetchall()
    
    response = make_response(jsonify(items))
    response.status_code = 200
    return response

@seller.route('/trade_history', methods=['GET'])
def get_trade_history():
    """
    GET /seller/trade_history

    Retrieves the trade history for a seller.
    Expects a query parameter 'seller_id' to filter trades.

    Returns:
        A JSON response containing a list of trades associated with the seller, including fields:
            - trade_id
            - item_id
            - trade_date
            - status
            - additional_cash (if applicable)
    """
    seller_id = request.args.get('seller_id')
    if not seller_id:
        return make_response(jsonify({"error": "seller_id query parameter is required"}), 400)
    
    query = """
        SELECT trade_id, item_id, trade_date, status, additional_cash
        FROM trades
        WHERE seller_id = %s
    """
    cursor = db.get_db().cursor()
    cursor.execute(query, (seller_id,))
    trade_history = cursor.fetchall()
    
    response = make_response(jsonify(trade_history))
    response.status_code = 200
    return response