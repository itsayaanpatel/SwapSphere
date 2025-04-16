##################################################
# This is the main/entry-point file for the 
# SwapSphere project application
##################################################

import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Users arriving at this page are not authenticated.
st.session_state['authenticated'] = False

# Ensure that the default sidebar navigation is turned off (see app/src/.streamlit/config.toml).
SideBarLinks(show_home=True)

st.title('SwapSphere – Your Smart Bartering Platform')
st.write('\n\n')
st.write('### Choose a persona to log in as:')

# Buyer (Jake)
if st.button("Act as Jake, a Buyer", type='primary', use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'buyer'
    st.session_state['first_name'] = 'Jake'
    logger.info("Logging in as Buyer (Jake)")
    st.switch_page('pages/00_Buyer_Home.py')

# Seller (Emma)
if st.button("Act as Emma, a Seller", type='primary', use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'seller'
    st.session_state['first_name'] = 'Emma'
    logger.info("Logging in as Seller (Emma)")
    st.switch_page('pages/10_Seller_Home.py')

# System Administrator (Lisa)
if st.button("Act as Lisa, the System Administrator", type='primary', use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'administrator'
    st.session_state['first_name'] = 'Lisa'
    logger.info("Logging in as System Administrator (Lisa)")
    st.switch_page('pages/20_Admin_Home.py')

# Data Analyst (Raj)
if st.button("Act as Raj, the Data Analyst", type='primary', use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'data_analyst'
    st.session_state['first_name'] = 'Raj'
    logger.info("Logging in as Data Analyst (Raj)")
    st.switch_page('pages/30_Data_Analyst_Home.py')
