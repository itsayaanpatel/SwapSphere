from flask import Blueprint, request, jsonify
from api.models import db, Trade

trades_bp = Blueprint('trades', __name__)

@trades_bp.route('/trades', methods=['POST'])
def create_trade():
    """Handle new trade creation [Jake-5], [Emma-3]"""
    try:
        data = request.get_json()
        new_trade = Trade(
            proposer_id=data['proposer_id'],
            receiver_id=data['receiver_id'],
            status='Proposed'
        )
        db.session.add(new_trade)
        db.session.commit()
        return jsonify({
            'id': new_trade.id,
            'status': new_trade.status
        }), 201  # HTTP 201 = Created
    except Exception as e:
        return jsonify({'error': str(e)}), 400  # HTTP 400 = Bad Request