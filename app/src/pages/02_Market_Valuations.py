import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title('Market Valuations')

response = requests.get("http://api:4000/market_valuations")
if response.status_code == 200:
    valuations = response.json()
    st.write("Real-Time Market Valuations:")
    st.dataframe(valuations)
else:
    st.error("Failed to fetch market valuations.")
