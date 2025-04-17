# trade_routes.py
from flask import Blueprint, request, jsonify, make_response
from backend.db_connection import db

negotiations = Blueprint('negotiations', __name__)

@negotiations.route('/negotiations/<int:trade_id>', methods=['GET'])
def get_trade(trade_id):
    cursor = db.get_db().cursor()
    cursor.execute(
        """
        SELECT trade_id, proposer_id, receiver_id, status, cash_adjustment, created_at
        FROM Trades
        WHERE trade_id = %s
        """, (trade_id,)
    )
    trade = cursor.fetchone()
    return make_response(jsonify(trade), 200)

@negotiations.route('/negotiations/<int:trade_id>/items', methods=['GET'])
def get_trade_items(trade_id):
    cursor = db.get_db().cursor()
    cursor.execute(
        """
        SELECT ti.item_id, i.title, i.estimated_value, u.username AS offered_by
        FROM Trade_Items ti
        JOIN Items i ON ti.item_id = i.item_id
        JOIN Users u ON ti.offered_by = u.user_id
        WHERE ti.trade_id = %s
        ORDER BY ti.offered_by DESC
        """, (trade_id,)
    )
    items = cursor.fetchall()
    return make_response(jsonify(items), 200)

@negotiations.route('/negotiations/<int:trade_id>/messages', methods=['GET'])
def get_messages(trade_id):
    cursor = db.get_db().cursor()
    cursor.execute(
        """
        SELECT m.message_id, m.sender_id, u.username AS sender_name, m.content, m.sent_at
        FROM Messages m
        JOIN Users u ON m.sender_id = u.user_id
        WHERE m.trade_id = %s
        ORDER BY m.sent_at
        """, (trade_id,)
    )
    messages = cursor.fetchall()
    return make_response(jsonify(messages), 200)

@negotiations.route('/negotiations/<int:trade_id>/messages', methods=['POST'])
def send_message(trade_id):
    data = request.json or {}
    sender_id = data.get('sender_id')
    content = data.get('content')
    if not sender_id or not content:
        return make_response(jsonify({'error': 'sender_id and content required'}), 400)
    cursor = db.get_db().cursor()
    cursor.execute(
        "INSERT INTO Messages (trade_id, sender_id, content) VALUES (%s, %s, %s)",
        (trade_id, sender_id, content)
    )
    db.get_db().commit()
    return make_response(jsonify({'message': 'sent'}), 201)

@negotiations.route('/negotiations/<int:trade_id>/status', methods=['PUT'])
def update_trade_status(trade_id):
    data = request.json or {}
    status = data.get('status')
    cash_adjustment = data.get('cash_adjustment')
    if status is None and cash_adjustment is None:
        return make_response(jsonify({'error': 'nothing to update'}), 400)
    fields, params = [], []
    if status is not None:
        fields.append('status = %s')
        params.append(status)
    if cash_adjustment is not None:
        fields.append('cash_adjustment = %s')
        params.append(cash_adjustment)
    params.append(trade_id)
    query = f"UPDATE Trades SET {', '.join(fields)} WHERE trade_id = %s"
    cursor = db.get_db().cursor()
    cursor.execute(query, tuple(params))
    db.get_db().commit()
    return make_response(jsonify({'message': 'updated'}), 200)