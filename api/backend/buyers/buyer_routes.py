from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

buyer = Blueprint('buyer', __name__)

# ------------------------------------------------------------
# Get all available items (for buyers to browse)
@buyer.route('/items', methods=['GET'])
def get_available_items():
    current_app.logger.info('GET /buyer/items route')
    
    buyer_id = request.args.get('buyer_id', type=int)
    category_filter = request.args.get('category', None)
    
    base_query = '''
        SELECT i.item_id, i.title, i.description, i.category, 
               i.estimated_value, u.username as seller, u.trust_score
        FROM Items i
        JOIN Users u ON i.user_id = u.user_id
        WHERE i.status = 'Available'
        AND i.user_id != %s
    '''
    params = [buyer_id]
    
    if category_filter:
        base_query += ' AND i.category = %s'
        params.append(category_filter)
    
    cursor = db.get_db().cursor()
    cursor.execute(base_query, params)
    
    columns = [col[0] for col in cursor.description]
    theData = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    return make_response(jsonify(theData), 200)

# ------------------------------------------------------------
# Propose a new trade (buyer initiates trade)
@buyer.route('/trades', methods=['POST'])
def propose_trade():
    current_app.logger.info('POST /buyer/trades route')
    trade_data = request.json
    
    required_fields = ['proposer_id', 'receiver_id', 'offered_items', 'requested_items']
    if not all(field in trade_data for field in required_fields):
        return make_response(
            jsonify({'error': 'Missing required fields'}),
            400
        )
    
    try:
        cursor = db.get_db().cursor()
        
        # Create the trade record
        cursor.execute('''
            INSERT INTO Trades 
            (proposer_id, receiver_id, status)
            VALUES (%s, %s, 'Proposed')
        ''', (
            trade_data['proposer_id'],
            trade_data['receiver_id']
        ))
        trade_id = cursor.lastrowid
        
        # Link offered items
        for item_id in trade_data['offered_items']:
            cursor.execute('''
                INSERT INTO Trade_Items 
                (trade_id, item_id, offered_by)
                VALUES (%s, %s, %s)
            ''', (trade_id, item_id, trade_data['proposer_id']))
            
            # Mark items as pending
            cursor.execute('''
                UPDATE Items SET status = 'Pending'
                WHERE item_id = %s
            ''', (item_id,))
        
        # Link requested items
        for item_id in trade_data['requested_items']:
            cursor.execute('''
                INSERT INTO Trade_Items 
                (trade_id, item_id, offered_by)
                VALUES (%s, %s, %s)
            ''', (trade_id, item_id, trade_data['receiver_id']))
        
        db.get_db().commit()
        
        return make_response(
            jsonify({
                'message': 'Trade proposed successfully',
                'trade_id': trade_id
            }),
            201
        )
    
    except Exception as e:
        db.get_db().rollback()
        return make_response(
            jsonify({'error': str(e)}),
            500
        )

# ------------------------------------------------------------
# Get buyer's active trades
@buyer.route('/trades/<user_id>', methods=['GET'])
def get_buyer_trades(user_id):
    current_app.logger.info(f'GET /buyer/trades/{user_id} route')
    
    cursor = db.get_db().cursor()
    
    cursor.execute('''
        SELECT t.trade_id, t.status, t.created_at,
               u.username as other_party
        FROM Trades t
        JOIN Users u ON (t.proposer_id = u.user_id OR t.receiver_id = u.user_id) AND u.user_id != %s
        WHERE t.proposer_id = %s OR t.receiver_id = %s
        ORDER BY t.created_at DESC
    ''', (user_id, user_id, user_id))
    
    trades = [dict(zip(
        [col[0] for col in cursor.description],
        row
    )) for row in cursor.fetchall()]
    
    return make_response(jsonify(trades), 200)