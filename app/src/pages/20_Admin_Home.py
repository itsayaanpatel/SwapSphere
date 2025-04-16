"""
20_Admin_Home.py

This homepage is designed for the System Administrator persona (e.g., Lisa).
It provides access to key administrative functions including:
  1. Viewing the System Dashboard for an overall platform health summary.
  2. Monitoring Fraud Reports to detect and address suspicious activity.
  3. Managing ML Models, including training and testing models.
  4. Managing User Accounts by flagging or updating user statuses.

Each button redirects to pages with further administrative functionalities.
"""

import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title(f"Welcome System Administrator, {st.session_state['first_name']}.")
st.write('### Select an administrative function:')

# Option 1: View System Dashboard (overview of platform health)
if st.button('View System Dashboard', type='primary', use_container_width=True):
    st.switch_page('pages/21_System_Dashboard.py')

# Option 2: Monitor Fraud Reports (view and manage flags)
if st.button('Monitor Fraud Reports', type='primary', use_container_width=True):
    st.switch_page('pages/22_Fraud_Reports.py')

# Option 3: Manage ML Models (train/test and view predictions)
if st.button('Manage ML Models', type='primary', use_container_width=True):
    st.switch_page('pages/23_ML_Model_Mgmt.py')

# Option 4: Manage User Accounts (flag or update users)
if st.button('Manage User Accounts', type='primary', use_container_width=True):
    st.switch_page('pages/24_User_Management.py')
