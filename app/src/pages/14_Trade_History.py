"""
14_Trade_History.py

This page displays the trade history for a seller by querying the
/seller/trade_history endpoint with the seller's user ID.
"""

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()

st.title("Your Trade History")

seller_id = st.session_state.get("user_id")
if not seller_id:
    seller_id = st.text_input("Enter your Seller ID:")

if seller_id:
    url = f"http://localhost:4000/seller/trade_history?seller_id={seller_id}"
    response = requests.get(url)
    if response.status_code == 200:
        trade_history = response.json()
        st.dataframe(trade_history)
    else:
        st.error("Failed to retrieve trade history.")
