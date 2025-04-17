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