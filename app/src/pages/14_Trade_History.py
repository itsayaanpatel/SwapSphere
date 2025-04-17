import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()

st.title("Your Trade History")

seller_id = st.session_state.get("user_id")
if not seller_id:
    seller_id = st.text_input("Enter your Seller ID:")

if seller_id:
    url = (f"http://api:4000/sellers/trade_history/{seller_id}")
    response = requests.get(url)
    if response.status_code == 200:
        try:
            # Try to convert response to DataFrame if it's JSON
            trade_history = response.json()
            df = pd.DataFrame(trade_history)
            st.dataframe(df)
        except ValueError:
            # If not JSON, display as text
            st.write(response.text)
    else:
        st.error("Failed to retrieve trade history.")