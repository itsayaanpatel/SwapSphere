from flask import Blueprint, request, jsonify, make_response
from backend.db_connection import db

# Create a new Blueprint object for trades
trades = Blueprint('trades', __name__)

# Get trades for a specific user
@trades.route('/trades/<user_id>', methods=['GET'])
def get_user_trades(user_id):
    cursor = db.get_db().cursor()
    query = f'''
        SELECT t.trade_id, t.proposer_id, t.receiver_id, t.status, t.fairness_score, t.cash_adjustment
        FROM Trades t
        WHERE t.proposer_id = {user_id} OR t.receiver_id = {user_id}
    '''
    cursor.execute(query)
    
    trades_data = cursor.fetchall()
    
    response = make_response(jsonify(trades_data))
    response.status_code = 200
    return response

# Get specific trade details by trade ID
@trades.route('/trades/details/<trade_id>', methods=['GET'])
def get_trade_details(trade_id):
    cursor = db.get_db().cursor()
    query = f'''
        SELECT t.trade_id, t.proposer_id, t.receiver_id, t.status, t.fairness_score, t.cash_adjustment
        FROM Trades t
        WHERE t.trade_id = {trade_id}
    '''
    cursor.execute(query)
    
    trade_data = cursor.fetchall()
    
    response = make_response(jsonify(trade_data))
    response.status_code = 200
    return response

# Update trade status, fairness score, and cash adjustment
@trades.route('/trades/<trade_id>', methods=['PUT'])
def update_trade_status(trade_id):
    trade_info = request.json
    status = trade_info['status']
    fairness_score = trade_info['fairness_score']
    cash_adjustment = trade_info['cash_adjustment']

    query = f'''
        UPDATE Trades 
        SET status = '{status}', fairness_score = {fairness_score}, cash_adjustment = {cash_adjustment}
        WHERE trade_id = {trade_id}
    '''
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return 'Trade status updated successfully!'
