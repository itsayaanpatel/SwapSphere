# routes/analytics_routes.py
from flask import Blueprint, jsonify, make_response, current_app
from backend.db_connection import db

analytics = Blueprint('analytics', __name__)


# Trade Frequency Over Time
@analytics.route('/analytics/trade-frequency', methods=['GET'])
def trade_frequency():
    current_app.logger.info('GET /analytics/trade-frequency')

    cursor = db.get_db().cursor()
    cursor.execute("""
        SELECT DATE(created_at) AS trade_date, COUNT(*) AS num_trades
        FROM Trades
        GROUP BY trade_date
        ORDER BY trade_date ASC
    """)
    
    # results = [dict(zip([col[0] for col in cursor.description], row))
    #            for row in cursor.fetchall()]
    
    results = cursor.fetchall()
    return make_response(jsonify(results), 200)


#Top Traded Categories
@analytics.route('/analytics/top-categories', methods=['GET'])
def top_traded_categories():
    current_app.logger.info('GET /analytics/top-categories')

    cursor = db.get_db().cursor()
    cursor.execute("""
        SELECT i.category, COUNT(*) AS times_traded
        FROM Trade_Items ti
        JOIN Items i ON ti.item_id = i.item_id
        GROUP BY i.category
        ORDER BY times_traded DESC
    """)

    # results = [dict(zip([col[0] for col in cursor.description], row))
    #            for row in cursor.fetchall()]
    results = cursor.fetchall()
    return make_response(jsonify(results), 200)


# Export Summary Report
@analytics.route('/analytics/export-summary', methods=['GET'])
def export_summary():
    current_app.logger.info('GET /analytics/export-summary')

    cursor = db.get_db().cursor()
    cursor.execute("SELECT COUNT(*) FROM Trades")
    total_trades = cursor.fetchone()

    cursor.execute("SELECT ROUND(AVG(fairness_score), 2) FROM Trades")
    avg_fairness = cursor.fetchone()

    cursor.execute("SELECT COUNT(*) FROM Fraud_Reports")
    total_reports = cursor.fetchone()

    summary = {
        "total_trades": total_trades,
        "average_fairness_score": avg_fairness,
        "total_fraud_reports": total_reports
    }

    return make_response(jsonify(summary), 200)
