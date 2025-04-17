from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

negotiation = Blueprint('negotiation', __name__)


# ------------------------------------------------------------
# Negotiate a deal with a buyer for a specific item
@negotiation.route('/negotiate', methods=['POST'])
def negotiate_deal():
    current_app.logger.info('POST /buyer/negotiate route')

    data = request.get_json()
    buyer_id = data.get('buyer_id')
    item_id = data.get('item_id')
    offer_price = data.get('offer_price')

    if not all([buyer_id, item_id, offer_price]):
        return make_response(jsonify({'error': 'Missing required fields'}), 400)

    cursor = db.get_db().cursor()

    # Fetch asking price of the item
    query = '''
        SELECT estimated_value
        FROM Items
        WHERE item_id = %s AND status = 'Available'
    '''
    cursor.execute(query, [item_id])
    result = cursor.fetchone()

    if not result:
        return make_response(jsonify({'error': 'Item not found or not available'}), 404)

    asking_price = result[0]

    # Simple negotiation logic
    if offer_price >= asking_price * 0.9:
        status = 'accepted'
        message = f'Offer of ${offer_price} accepted for item {item_id}.'
    else:
        counter_offer = round(asking_price * 0.95, 2)
        status = 'counter'
        message = f'Offer too low. Counter-offer is ${counter_offer}.'

    response = {
        'status': status,
        'message': message
    }

    return make_response(jsonify(response), 200)
