#------------------------------------------------------------
# Get all available items (for buyers to browse)
#   Filters out items already owned by the buyer
@buyer.route('/buyer/items', methods=['GET'])
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
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Propose a new trade (buyer initiates trade)
#   Creates trade record and links items
@buyer.route('/buyer/trades', methods=['POST'])
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
            (proposer_id, receiver_id, status, fairness_score)
            VALUES (%s, %s, 'Proposed', %s)
        ''', (
            trade_data['proposer_id'],
            trade_data['receiver_id'],
            trade_data.get('fairness_score', 0)
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
            
            # Mark items as pending
            cursor.execute('''
                UPDATE Items SET status = 'Pending'
                WHERE item_id = %s
            ''', (item_id,))
        
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

#------------------------------------------------------------
# Get all trades where user is the buyer (proposer)
#   Includes trade details and item information
@buyer.route('/buyer/trades/<userID>', methods=['GET'])
def get_buyer_trades(userID):
    current_app.logger.info(f'GET /buyer/trades/{userID} route')
    
    cursor = db.get_db().cursor()
    
    # Get basic trade info
    cursor.execute('''
        SELECT t.trade_id, t.status, t.fairness_score, t.created_at,
               u.username as receiver_name, u.trust_score as receiver_trust_score
        FROM Trades t
        JOIN Users u ON t.receiver_id = u.user_id
        WHERE t.proposer_id = %s
        ORDER BY t.created_at DESC
    ''', (userID,))
    
    trades = [dict(zip(
        [col[0] for col in cursor.description],
        row
    )) for row in cursor.fetchall()]
    
    # Get items for each trade
    for trade in trades:
        cursor.execute('''
            SELECT i.item_id, i.title, i.estimated_value, 
                   ti.offered_by, u.username as offered_by_username
            FROM Trade_Items ti
            JOIN Items i ON ti.item_id = i.item_id
            JOIN Users u ON ti.offered_by = u.user_id
            WHERE ti.trade_id = %s
        ''', (trade['trade_id'],))
        
        trade['items'] = [dict(zip(
            [col[0] for col in cursor.description],
            row
        )) for row in cursor.fetchall()]
    
    the_response = make_response(jsonify(trades))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Cancel a proposed trade (buyer withdraws offer)
#   Only allowed if trade is still in Proposed state
@buyer.route('/buyer/trades/<tradeID>', methods=['DELETE'])
def cancel_trade(tradeID):
    current_app.logger.info(f'DELETE /buyer/trades/{tradeID} route')
    
    cursor = db.get_db().cursor()
    
    # Check trade status
    cursor.execute('''
        SELECT status, proposer_id 
        FROM Trades 
        WHERE trade_id = %s
    ''', (tradeID,))
    trade = cursor.fetchone()
    
    if not trade:
        return make_response(
            jsonify({'error': 'Trade not found'}),
            404
        )
    
    if trade[0] != 'Proposed':
        return make_response(
            jsonify({'error': 'Only proposed trades can be canceled'}),
            400
        )
    
    # Get items involved in trade
    cursor.execute('''
        SELECT item_id, offered_by 
        FROM Trade_Items 
        WHERE trade_id = %s
    ''', (tradeID,))
    trade_items = cursor.fetchall()
    
    try:
        # Update items status back to Available
        for item_id, offered_by in trade_items:
            cursor.execute('''
                UPDATE Items 
                SET status = 'Available'
                WHERE item_id = %s
            ''', (item_id,))
        
        # Delete trade items
        cursor.execute('''
            DELETE FROM Trade_Items 
            WHERE trade_id = %s
        ''', (tradeID,))
        
        # Delete trade
        cursor.execute('''
            DELETE FROM Trades 
            WHERE trade_id = %s
        ''', (tradeID,))
        
        db.get_db().commit()
        
        return make_response(
            jsonify({'message': 'Trade canceled successfully'}),
            200
        )
    
    except Exception as e:
        db.get_db().rollback()
        return make_response(
            jsonify({'error': str(e)}),
            500
        )

#------------------------------------------------------------
# Send message about a trade (buyer communicates with seller)
#   Records message and links to trade
@buyer.route('/buyer/messages', methods=['POST'])
def send_message():
    current_app.logger.info('POST /buyer/messages route')
    message_data = request.json
    
    required_fields = ['sender_id', 'receiver_id', 'trade_id', 'content']
    if not all(field in message_data for field in required_fields):
        return make_response(
            jsonify({'error': 'Missing required fields'}),
            400
        )
    
    cursor = db.get_db().cursor()
    cursor.execute('''
        INSERT INTO Messages 
        (sender_id, receiver_id, trade_id, content)
        VALUES (%s, %s, %s, %s)
    ''', (
        message_data['sender_id'],
        message_data['receiver_id'],
        message_data['trade_id'],
        message_data['content']
    ))
    db.get_db().commit()
    
    return make_response(
        jsonify({
            'message': 'Message sent successfully',
            'message_id': cursor.lastrowid
        }),
        201
    )

#------------------------------------------------------------
# Get trade messages (buyer views conversation)
#   Paginated message history for a specific trade
@buyer.route('/buyer/trades/<tradeID>/messages', methods=['GET'])
def get_trade_messages(tradeID):
    current_app.logger.info(f'GET /buyer/trades/{tradeID}/messages route')
    
    limit = request.args.get('limit', 50, type=int)
    offset = request.args.get('offset', 0, type=int)
    
    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT m.message_id, m.content, m.sent_at,
               s.username as sender, r.username as receiver
        FROM Messages m
        JOIN Users s ON m.sender_id = s.user_id
        JOIN Users r ON m.receiver_id = r.user_id
        WHERE m.trade_id = %s
        ORDER BY m.sent_at DESC
        LIMIT %s OFFSET %s
    ''', (tradeID, limit, offset))
    
    messages = [dict(zip(
        [col[0] for col in cursor.description],
        row
    )) for row in cursor.fetchall()]
    
    the_response = make_response(jsonify(messages))
    the_response.status_code = 200
    return the_response