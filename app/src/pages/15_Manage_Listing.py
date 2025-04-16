"""
15_Manage_Listings.py

This page enables sellers to manage their inventory listings.
It displays all items for the seller via the /seller/items endpoint and
provides options to update or delete each item.
"""

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()

st.title("Manage Inventory Listings")

seller_id = st.session_state.get("user_id")
if not seller_id:
    seller_id = st.text_input("Enter your Seller ID:")

if seller_id:
    url = f"http://api:4000/seller/items?seller_id={seller_id}"
    response = requests.get(url)
    if response.status_code == 200:
        items = response.json()
        st.write("Your current items:")
        for item in items:
            st.markdown(f"**{item['title']}** (ID: {item['item_id']})")
            st.write(f"Category: {item['category']} | Value: ${item['estimated_value']} | Status: {item['status']}")
            with st.form(key=f"update_form_{item['item_id']}"):
                new_title = st.text_input("Title", value=item['title'])
                new_description = st.text_area("Description", value=item['description'])
                new_category = st.text_input("Category", value=item['category'])
                new_value = st.number_input("Estimated Value ($)", value=float(item['estimated_value']), step=1.0, format="%.2f")
                submit_update = st.form_submit_button("Update Item")
                if submit_update:
                    update_url = f"http://api:4000/seller/items/{item['item_id']}"
                    update_payload = {
                        "title": new_title,
                        "description": new_description,
                        "category": new_category,
                        "estimated_value": new_value,
                        "status": item.get("status", "Available")
                    }
                    update_response = requests.put(update_url, json=update_payload)
                    if update_response.status_code == 200:
                        st.success("Item updated successfully!")
                    else:
                        st.error("Failed to update item.")
            if st.button("Delete Item", key=f"delete_{item['item_id']}"):
                delete_url = f"http://api:4000/seller/items/{item['item_id']}"
                delete_response = requests.delete(delete_url)
                if delete_response.status_code == 200:
                    st.success("Item deleted successfully!")
                else:
                    st.error("Failed to delete item.")
            st.divider()
    else:
        st.error("Failed to fetch items.")
