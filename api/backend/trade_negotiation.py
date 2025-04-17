# pages/04_Buyer_Negotiation.py
from flask import Blueprint
import streamlit as st
from modules.nav import SideBarLinks
from backend.db_connection import db
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db
from backend.ml_models.model01 import predict

st.set_page_config(layout="wide")
SideBarLinks()

trade_negotiation = Blueprint('trade_negotiation', __name__)

# --- Initialize Session ---
if 'trade_id' not in st.session_state:
    st.session_state.trade_id = None

# --- Database Functions ---
def get_trade_details(trade_id):
    with db.cursor(dictionary=True) as cursor:
        cursor.execute("""
            SELECT t.*, 
                   p.username as proposer_name,
                   r.username as receiver_name
            FROM Trades t
            JOIN Users p ON t.proposer_id = p.user_id
            JOIN Users r ON t.receiver_id = r.user_id
            WHERE t.trade_id = %s
        """, (trade_id,))
        return cursor.fetchone()

def get_trade_items(trade_id):
    with db.cursor(dictionary=True) as cursor:
        cursor.execute("""
            SELECT ti.*, i.title, i.estimated_value, u.username
            FROM Trade_Items ti
            JOIN Items i ON ti.item_id = i.item_id
            JOIN Users u ON ti.offered_by = u.user_id
            WHERE ti.trade_id = %s
        """, (trade_id,))
        return cursor.fetchall()

def get_messages(trade_id):
    with db.cursor(dictionary=True) as cursor:
        cursor.execute("""
            SELECT m.*, u.username as sender_name
            FROM Messages m
            JOIN Users u ON m.sender_id = u.user_id
            WHERE m.trade_id = %s
            ORDER BY m.sent_at
        """, (trade_id,))
        return cursor.fetchall()

def send_message(trade_id, sender_id, content):
    with db.cursor() as cursor:
        cursor.execute("""
            INSERT INTO Messages 
            (sender_id, receiver_id, trade_id, content)
            VALUES (%s, %s, %s, %s)
        """, (
            sender_id,
            st.session_state.receiver_id,
            trade_id,
            content
        ))
        db.commit()

