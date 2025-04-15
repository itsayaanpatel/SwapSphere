import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Display customized sidebar links based on the buyer role.
SideBarLinks()

st.title(f"Welcome Buyer, {st.session_state['first_name']}.")
st.write('')
st.write('### What would you like to do today?')

# Buyer Use Case: View Trade Matching Recommendations
if st.button('View Trade Matching Recommendations', type='primary', use_container_width=True):
    # This page should later be updated to show AI-based trade matching features.
    st.switch_page('pages/01_Trade_Matching.py')

# Buyer Use Case: View Real-Time Market Valuations
if st.button('View Real-Time Market Valuations', type='primary', use_container_width=True):
    # This page should later be updated with market data and valuation tools.
    st.switch_page('pages/02_Market_Valuations.py')
