import streamlit as st
import requests
from datetime import datetime

from modules.nav import SideBarLinks
st.set_page_config(layout='wide')
SideBarLinks()

def show():
    st.title("💬 Negotiation Console")
    st.markdown("Communicate with sellers and finalize deals")
    
    # Get active negotiations from API
    negotiations = requests.get(
        f"http://api:5000/api/negotiations/user/{st.session_state.user_id}"
    ).json()
    
    # Section 1: Active Chats
    with st.expander("📨 Active Negotiations", expanded=True):
        selected_negotiation = st.selectbox(
            "Select Conversation",
            [f"Deal #{n['id']} - {n['item_name']}" for n in negotiations],
            index=0
        )
        
        # Display chat history
        negotiation_id = selected_negotiation.split("#")[1].split(" ")[0]
        messages = requests.get(
            f"http://api:5000/api/negotiations/{negotiation_id}/messages"
        ).json()
        
        for msg in messages:
            col = st.columns([1, 4])
            if msg["is_you"]:  # User's messages aligned right
                with col[1]:
                    st.markdown(f"""
                    <div style='background:#E1F5FE;padding:8px;border-radius:8px;margin:4px;'>
                    <small>{msg["timestamp"]}</small><br>
                    {msg["content"]}
                    </div>
                    """, unsafe_allow_html=True)
            else:  # Seller's messages aligned left
                with col[0]:
                    st.markdown(f"""
                    <div style='background:#F5F5F5;padding:8px;border-radius:8px;margin:4px;'>
                    <small>{msg["timestamp"]}</small><br>
                    {msg["content"]}
                    </div>
                    """, unsafe_allow_html=True)
        
        # Message input
        new_message = st.text_area("Type your message...", key="chat_input")
        if st.button("Send Message"):
            requests.post(
                f"http://api:5000/api/negotiations/{negotiation_id}/messages",
                json={
                    "content": new_message,
                    "sender_id": st.session_state.user_id
                }
            )
            st.rerun()
    
    # Section 2: Deal Actions
    with st.expander("🤝 Deal Terms", expanded=True):
        current_deal = next(n for n in negotiations if str(n["id"]) == negotiation_id)
        
        st.write(f"**Item:** {current_deal['item_name']}")
        st.write(f"**Current Offer:** ${current_deal['current_offer']:,.2f}")
        
        col1, col2 = st.columns(2)
        with col1:
            new_offer = st.number_input(
                "Your Counter Offer",
                min_value=0.0,
                value=float(current_deal['current_offer']),
                step=10.0
            )
        with col2:
            st.write("")  # Spacer
            if st.button("Submit Offer", type="primary"):
                response = requests.put(
                    f"http://api:5000/api/negotiations/{negotiation_id}",
                    json={"new_offer": new_offer}
                )
                st.success("Offer submitted!")
        
        if st.button("🔄 Refresh Chat", key="refresh_chat"):
            st.rerun()