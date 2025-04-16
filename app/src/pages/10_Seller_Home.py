"""
10_Seller_Home.py

This homepage is designed for the Seller persona (e.g., Emma).
It provides options for sellers to manage and optimize their trade listings.
The options include:
  1. Bulk Upload Items to list new products.
  2. View Trade History to track past deals.
  3. Manage Inventory Listings to edit item details or view auto-matching suggestions.

Each button navigates to a page dedicated to the respective functionality.
"""

import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Display sidebar links appropriate for a Seller.
SideBarLinks()

st.title(f"Welcome Seller, {st.session_state['first_name']}.")
st.write('')
st.write('### What would you like to do today?')

# Seller Use Case: Upload New Items
if st.button('Upload New Items', type='primary', use_container_width=True):
    # This page should later implement functionality for bulk uploading or individual item uploads.
    st.switch_page('pages/13_Upload_Items.py')

# Seller Use Case: View Trade History
if st.button('View Trade History', type='primary', use_container_width=True):
    # This page should show past trades and transaction history.
    st.switch_page('pages/14_Trade_History.py')

# Seller Use Case: Manage Listings
if st.button("Manage Inventory Listings", type='primary', use_container_width=True):
    # This page should let the seller update item details, get auto-matching suggestions, or analyze deals.
    st.switch_page('pages/15_Manage_Listings.py')
