import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title('View My Trades')

user_id = st.text_input("Enter Your User ID")

if user_id:
    response = requests.get(f"http://localhost:4000/trades/{user_id}")
    if response.status_code == 200:
        trades = response.json()
        st.write("Your Trades:")
        st.dataframe(trades)
    else:
        st.error("Failed to fetch trades.")