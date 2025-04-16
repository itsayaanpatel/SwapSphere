"""
13_Upload_Items.py

This page allows a seller to add (upload) new items into their inventory.
It uses a form to capture details (title, description, category,
estimated value) and sends a POST request to the /seller/items endpoint.
"""

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()

st.title("Upload New Items")

# Try to get the seller's user_id from session state; otherwise, ask for it.
seller_id = st.session_state.get("user_id")
if not seller_id:
    seller_id = st.text_input("Enter your Seller ID:")

with st.form("upload_item_form"):
    st.subheader("Item Details")
    title = st.text_input("Item Title")
    description = st.text_area("Description")
    category = st.text_input("Category")
    estimated_value = st.number_input("Estimated Value ($)", min_value=0.0, format="%.2f")
    submit = st.form_submit_button("Upload Item")

    if submit:
        payload = {
            "seller_id": seller_id,
            "title": title,
            "description": description,
            "category": category,
            "estimated_value": estimated_value
        }
        response = requests.post("http://api:4000/seller/items", json=payload)
        if response.status_code == 200:
            st.success("Item uploaded successfully!")
        else:
            st.error(f"Failed to upload item: {response.text}")
