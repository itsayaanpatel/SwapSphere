from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

buyer = Blueprint('buyer', __name__)

# Get all available items to browse
@buyer.route('/items', methods=['GET'])
def get_items():
    cursor = db.get_db().cursor()
    
    query = '''
        SELECT i.item_id, i.title, i.description, i.category, 
               i.estimated_value, u.username, u.trust_score
        FROM Items i
        JOIN Users u ON i.user_id = u.user_id
        WHERE i.status = 'Available'
    '''
    
    # Simple filtering
    if request.args.get('category'):
        query += " AND i.category = '{}'".format(request.args.get('category'))
    
    cursor.execute(query)
    items = cursor.fetchall()
    
    return make_response(jsonify(items), 200)

# Get trade recommendations for a buyer
@buyer.route('/recommendations/<user_id>', methods=['GET'])
def get_recommendations(user_id):
    cursor = db.get_db().cursor()
    
    cursor.execute('''
        SELECT i.*, u.username
        FROM Items i
        JOIN Users u ON i.user_id = u.user_id
        WHERE i.status = 'Available' 
        AND i.user_id != %s
        ORDER BY u.trust_score DESC
        LIMIT 10
    ''', (user_id,))
    
    recommendations = cursor.fetchall()
    return make_response(jsonify(recommendations), 200)

# Propose a new trade
@buyer.route('/trades', methods=['POST'])
def propose_trade():
    data = request.json
    
    cursor = db.get_db().cursor()
    
    # Simple fairness calculation
    cursor.execute('SELECT SUM(estimated_value) FROM Items WHERE item_id IN %s', 
                  [tuple(data['your_items'])])
    your_value = cursor.fetchone()['SUM(estimated_value)'] or 0
    
    cursor.execute('SELECT SUM(estimated_value) FROM Items WHERE item_id IN %s', 
                  [tuple(data['their_items'])])
    their_value = cursor.fetchone()['SUM(estimated_value)'] or 0
    
    fairness = min(your_value, their_value) / max(your_value, 1) * 100
    
    # Create trade
    cursor.execute('''
        INSERT INTO Trades (proposer_id, receiver_id, status, fairness_score)
        VALUES (%s, %s, 'Proposed', %s)
    ''', (data['your_id'], data['their_id'], fairness))
    trade_id = cursor.lastrowid
    
    # Add items to trade
    for item_id in data['your_items']:
        cursor.execute('''
            INSERT INTO Trade_Items (trade_id, item_id, offered_by)
            VALUES (%s, %s, %s)
        ''', (trade_id, item_id, data['your_id']))
    
    for item_id in data['their_items']:
        cursor.execute('''
            INSERT INTO Trade_Items (trade_id, item_id, offered_by)
            VALUES (%s, %s, %s)
        ''', (trade_id, item_id, data['their_id']))
    
    db.get_db().commit()
    
    return make_response(jsonify({
        'message': 'Trade proposed!',
        'trade_id': trade_id,
        'fairness_score': fairness
    }), 201)

# Get buyer's active trades
@buyer.route('/trades/<user_id>', methods=['GET'])
def get_trades(user_id):
    cursor = db.get_db().cursor()
    
    cursor.execute('''
        SELECT t.*, u.username as other_user
        FROM Trades t
        JOIN Users u ON (t.proposer_id = u.user_id OR t.receiver_id = u.user_id) AND u.user_id != %s
        WHERE t.proposer_id = %s OR t.receiver_id = %s
    ''', (user_id, user_id, user_id))
    
    trades = cursor.fetchall()
    return make_response(jsonify(trades), 200)