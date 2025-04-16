"""
00_Buyer_Home.py

This homepage is designed for the Buyer persona (e.g., Jake).
It displays a personalized greeting along with three key options:
  1. View Trade Matching Recommendations (AI-powered matching based on the buyer's wishlist)
  2. View Real-Time Market Valuations (to help ensure fair pricing)
  3. Negotiate Partial Cash Deals (for trades where item values do not match exactly)

Each option redirects the user to the corresponding page for detailed functionality.
"""
import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Display customized sidebar links for the Buyer role.
SideBarLinks(show_home=True)

st.title(f"Welcome Buyer, {st.session_state['first_name']}.")
st.write('### What would you like to do today?')

# Option 1: View Trade Matching Recommendations (AI-powered matching)
if st.button('View Trade Matching Recommendations', type='primary', use_container_width=True):
    st.switch_page('pages/01_Trade_Matching.py')

# Option 2: View Real-Time Market Valuations (for fair pricing)
if st.button('View Real-Time Market Valuations', type='primary', use_container_width=True):
    st.switch_page('pages/02_Market_Valuations.py')

# Option 3: Negotiate Partial Cash Deals (if values don’t match exactly)
if st.button('Negotiate Partial Cash Deals', type='primary', use_container_width=True):
    st.switch_page('pages/03_Negotiate_Deal.py')
