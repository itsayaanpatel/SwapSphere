"""
30_Data_Analyst_Home.py

This homepage is designed for the Data Analyst persona (e.g., Raj).
It provides functionality for analyzing platform data, including:
  1. Viewing Trade Frequency Trends to gain insights on overall trade volume.
  2. Viewing the Most-Traded Item Categories to help refine recommendation algorithms.
  3. Exporting Analytics Reports for sharing data-driven insights with stakeholders.

Each option leads to pages that implement these analytical tasks.
"""

import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title(f"Welcome Data Analyst, {st.session_state['first_name']}.")
st.write('### Select an analytical function:')

# Option 1: View Trade Frequency Trends (for data insights)
if st.button('View Trade Frequency Trends', type='primary', use_container_width=True):
    st.switch_page('pages/31_Trade_Frequency.py')

# Option 2: View Most-Traded Item Categories (to refine recommendations)
if st.button('View Most-Traded Item Categories', type='primary', use_container_width=True):
    st.switch_page('pages/32_Trade_Categories.py')

# Option 3: Export Analytics Reports (for sharing insights)
if st.button('Export Analytics Reports', type='primary', use_container_width=True):
    st.switch_page('pages/33_Export_Reports.py')
