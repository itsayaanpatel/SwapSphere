
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db
from backend.ml_models.model01 import predict

# Create Blueprint object for market valuations

market_valuations = Blueprint('market_valuations', __name__)


# Get real-time market valuations for all items
@market_valuations.route('/market_valuations', methods=['GET'])
def get_market_valuations():
    cursor = db.get_db().cursor()
    query = '''
        SELECT item_id, title, estimated_value, category
        FROM Items
        WHERE status = 'Available'
    '''
    cursor.execute(query)
    
    valuations = cursor.fetchall()
    
    response = make_response(jsonify(valuations))
    response.status_code = 200
    return response
