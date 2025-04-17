
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db
from backend.ml_models.model01 import predict


# Create  new Blueprint object for negotiating cash deals
cash_deals = Blueprint('cash_deals', __name__)

# Get trade details and allow the user to propose a cash deal
@cash_deals.route('/negotiate_deal/<trade_id>', methods=['GET'])
def negotiate_cash_deal(trade_id):
    cursor = db.get_db().cursor()
    query = f'''
        SELECT t.trade_id, t.proposer_id, t.receiver_id, t.status, t.fairness_score, t.cash_adjustment
        FROM Trades t
        WHERE t.trade_id = {trade_id} AND t.status = 'Available'
    '''
    cursor.execute(query)
    
    trade_data = cursor.fetchall()
    
    response = make_response(jsonify(trade_data))
    response.status_code = 200
    return response

# Update the cash deal with a partial cash adjustment proposal
@cash_deals.route('/negotiate_deal/<trade_id>', methods=['PUT'])
def update_cash_deal(trade_id):
    deal_info = request.json
    cash_adjustment = deal_info['cash_adjustment']

    query = f'''
        UPDATE Trades
        SET cash_adjustment = {cash_adjustment}
        WHERE trade_id = {trade_id}
    '''
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return 'Cash adjustment updated successfully!'
