# pages/05_Trade_Negotiation.py
import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()
st.title("Trade Negotiation")

# Base API URL (can be overridden in session state)
API_BASE = st.session_state.get('api_base', 'http://api:4000')

# --- Step 1: Get User ID ---
user_id = st.text_input("Enter Your User ID:")
if not user_id:
    st.info("Please enter your User ID to load your trades.")
    st.stop()

# --- Step 2: Fetch all active trades for this user ---
try:
    trades_resp = requests.get(f"{API_BASE}/trades/{user_id}")
    trades_resp.raise_for_status()
    trades = trades_resp.json()
except Exception as e:
    st.error(f"Failed to fetch trades: {e}")
    st.stop()

if not trades:
    st.warning("No active trades found for this user.")
    st.stop()

# --- Step 3: Select a trade ---
trade_options = [f"Trade #{t['trade_id']} (with {t.get('other_party','')}): {t['status']}" for t in trades]
selection = st.selectbox("Select a trade to negotiate:", trade_options)
selected_index = trade_options.index(selection)
trade_id = trades[selected_index]['trade_id']
trade = trades[selected_index]

# --- Step 4: Fetch trade-specific data ---
# Items
try:
    items_resp = requests.get(f"{API_BASE}/negotiations/{trade_id}/items")
    items_resp.raise_for_status()
    items = items_resp.json()
except:
    items = []

# Messages
try:
    msg_resp = requests.get(f"{API_BASE}/negotiations/{trade_id}/messages")
    msg_resp.raise_for_status()
    messages = msg_resp.json()
except:
    messages = []

# Determine other party ID
proposer = trade.get('proposer_id')
receiver = trade.get('receiver_id')
other_id = receiver if str(user_id) == str(proposer) else proposer

# --- Layout Tabs ---
tab1, tab2 = st.tabs(["Conversation", "Details & Items"])

with tab1:
    st.subheader("Chat History")
    for m in messages:
        is_me = str(m['sender_id']) == str(user_id)
        role = 'user' if is_me else 'assistant'
        with st.chat_message(role):
            st.markdown(f"**{m['sender_name']}** ({m['sent_at']}):")
            st.write(m['content'])

    if trade['status'] in ['Proposed', 'Pending']:
        user_msg = st.chat_input("Type a message...")
        if user_msg:
            payload = {'sender_id': user_id, 'content': user_msg}
            post_resp = requests.post(f"{API_BASE}/negotiations/{trade_id}/messages", json=payload)
            if post_resp.ok:
                st.experimental_rerun()
            else:
                st.error("Failed to send message.")

with tab2:
    st.subheader("Trade Details")
    st.write(f"**Status:** {trade['status']}")
    st.write(f"**Cash Adjustment:** ${trade.get('cash_adjustment', 0)}")

    st.markdown("---")
    st.subheader("Items Exchanged")
    col1, col2 = st.columns(2)
    your_items = [i for i in items if str(i['offered_by']) == str(user_id)]
    their_items = [i for i in items if str(i['offered_by']) != str(user_id)]

    with col1:
        st.markdown("**Your Items**")
        for it in your_items:
            st.write(f"- {it['title']} (${it['estimated_value']})")
    with col2:
        st.markdown("**Their Items**")
        for it in their_items:
            st.write(f"- {it['title']} (${it['estimated_value']}) by User {it['offered_by']}")

    # Actions
    if trade['status'] == 'Proposed':
        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Accept Trade"):
                resp = requests.put(f"{API_BASE}/negotiations/{trade_id}/status", json={'status':'Accepted'})
                if resp.ok:
                    st.success("Trade accepted.")
                    st.experimental_rerun()
                else:
                    st.error("Failed to accept trade.")
        with c2:
            new_amt = st.number_input("Propose Cash Adjustment ($)", value=float(trade.get('cash_adjustment',0)))
            if st.button("Counteroffer"):
                upd = {'status':'Countered', 'cash_adjustment': new_amt}
                resp = requests.put(f"{API_BASE}/negotiations/{trade_id}/status", json=upd)
                if resp.ok:
                    st.success("Counteroffer sent.")
                    st.experimental_rerun()
                else:
                    st.error("Failed to send counteroffer.")
