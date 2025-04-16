# pages/04_Buyer_Negotiation.py
import streamlit as st
from modules.nav import SideBarLinks
from backend.db_connection import db
import datetime

st.set_page_config(layout="wide")
SideBarLinks()

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

# --- UI Components ---
def display_item_comparison(items):
    your_items = [i for i in items if i['offered_by'] == st.session_state.user_id]
    their_items = [i for i in items if i['offered_by'] != st.session_state.user_id]
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Your Items")
        for item in your_items:
            with st.container(border=True):
                st.write(f"**{item['title']}**")
                st.write(f"Value: ${item['estimated_value']}")
    
    with col2:
        st.subheader("Their Items")
        for item in their_items:
            with st.container(border=True):
                st.write(f"**{item['title']}**")
                st.write(f"Value: ${item['estimated_value']}")
                st.write(f"From: {item['username']}")

# --- Main UI ---
st.title("Trade Negotiation")

if 'user_id' not in st.session_state:
    st.error("Please login first")
    st.stop()

if not st.session_state.trade_id:
    st.warning("No trade selected. Redirecting...")
    st.switch_page("pages/01_Trade_Matching.py")
    st.stop()

trade = get_trade_details(st.session_state.trade_id)
items = get_trade_items(st.session_state.trade_id)
messages = get_messages(st.session_state.trade_id)

# Set receiver ID (the other party)
if st.session_state.user_id == trade['proposer_id']:
    st.session_state.receiver_id = trade['receiver_id']
else:
    st.session_state.receiver_id = trade['proposer_id']

# --- Layout ---
tab1, tab2 = st.tabs(["Negotiation", "Trade Details"])

with tab1:
    # Message History
    st.subheader("Conversation")
    for msg in messages:
        with st.chat_message("user" if msg['sender_id'] == st.session_state.user_id else "assistant"):
            st.write(f"**{msg['sender_name']}** ({msg['sent_at'].strftime('%H:%M')})")
            st.write(msg['content'])
    
    # New Message
    if trade['status'] in ['Proposed', 'Pending']:
        new_msg = st.chat_input("Type your message...")
        if new_msg:
            send_message(st.session_state.trade_id, st.session_state.user_id, new_msg)
            st.rerun()

with tab2:
    display_item_comparison(items)
    
    if trade['status'] == 'Proposed':
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Accept Trade", type="primary"):
                # Update trade status
                pass
        with col2:
            cash_adjust = st.number_input("Cash Adjustment ($)", 
                                        value=float(trade['cash_adjustment']))
            if st.button("Make Counteroffer"):
                # Update trade with new terms
                pass