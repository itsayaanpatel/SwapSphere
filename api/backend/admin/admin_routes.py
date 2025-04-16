"""
admin_routes.py

Combined admin blueprint with all system administration endpoints:
 - User management (/users)
 - Analytics (/analytics/trends, /analytics/fraud, /logs)
 - Fraud report management (/fraud_reports)
 - ML model operations (/c/train, /c/test)
"""
from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db
from backend.ml_models.model01 import train, test

admin_bp = Blueprint('admin_bp', __name__)

# ----- User Management -----
@admin_bp.route('/users', methods=['GET'])
def get_users():
    """Return list of all users with basic info."""
    cursor = db.get_db().cursor()
    cursor.execute("""
        SELECT user_id, username, email, trust_score
        FROM Users
    """)
    users = cursor.fetchall()
    return make_response(jsonify(users), 200)

@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update a user’s trust_score."""
    data = request.json or {}
    if 'trust_score' not in data:
        return make_response(jsonify({'error': 'trust_score required'}), 400)
    cursor = db.get_db().cursor()
    cursor.execute(
        "UPDATE Users SET trust_score = %s WHERE user_id = %s",
        (data['trust_score'], user_id)
    )
    db.get_db().commit()
    return make_response(jsonify({'message': 'User updated'}), 200)


# ----- Trade Metrics -----
@admin_bp.route('/trades/count', methods=['GET'])
def trade_count():
    """Return total number of trades."""
    cursor = db.get_db().cursor()
    cursor.execute("SELECT COUNT(*) AS total_trades FROM Trades")
    row = cursor.fetchone()
    return make_response(jsonify(row), 200)

@admin_bp.route('/trades/average_daily', methods=['GET'])
def average_daily_trades():
    """Return average number of trades per day."""
    cursor = db.get_db().cursor()
    cursor.execute("""
        SELECT 
          ROUND(AVG(daily_count),2) AS avg_trades_per_day
        FROM (
          SELECT DATE(created_at) AS day, COUNT(*) AS daily_count
          FROM Trades
          GROUP BY DATE(created_at)
        ) sub
    """)
    row = cursor.fetchone()
    return make_response(jsonify(row), 200)


# ----- System Logs -----
@admin_bp.route('/logs', methods=['GET'])
def system_logs():
    """Return recent system logs."""
    cursor = db.get_db().cursor()
    cursor.execute("""
        SELECT log_id, user_id, action, log_time
        FROM Logs
        ORDER BY log_time DESC
        LIMIT 50
    """)
    rows = cursor.fetchall()
    return make_response(jsonify(rows), 200)


# ----- Fraud Reports -----
@admin_bp.route('/fraud_reports', methods=['GET'])
def list_reports():
    """List all fraud reports."""
    cursor = db.get_db().cursor()
    cursor.execute("""
        SELECT report_id, trade_id, reported_by, reason, status, created_at
        FROM Fraud_Reports
        ORDER BY created_at DESC
    """)
    rows = cursor.fetchall()
    return make_response(jsonify(rows), 200)

@admin_bp.route('/fraud_reports/<int:report_id>', methods=['PUT'])
def update_report(report_id):
    """Update status of a fraud report."""
    data = request.json or {}
    status = data.get('status')
    if status not in ('Under Review','Resolved','Dismissed'):
        return make_response(jsonify({'error':'Invalid status'}), 400)
    cursor = db.get_db().cursor()
    cursor.execute(
        "UPDATE Fraud_Reports SET status = %s WHERE report_id = %s",
        (status, report_id)
    )
    db.get_db().commit()
    return make_response(jsonify({'message':'Report updated'}), 200)


# ----- ML Model Management -----
@admin_bp.route('/c/train', methods=['POST'])
def train_model():
    """Trigger training of ML Model 01."""
    try:
        result = train()
        return make_response(jsonify({'message': result}), 200)
    except Exception as e:
        current_app.logger.error(f"Training error: {e}")
        return make_response(jsonify({'error': str(e)}), 500)

@admin_bp.route('/c/test', methods=['POST'])
def test_model():
    """Trigger testing of ML Model 01."""
    try:
        result = test()
        return make_response(jsonify({'message': result}), 200)
    except Exception as e:
        current_app.logger.error(f"Testing error: {e}")
        return make_response(jsonify({'error': str(e)}), 500)
