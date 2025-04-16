"""
14_Seller_Profile.py

Simple seller profile display page.
"""

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()  # Show sidebar links

st.title("Your Profile")

# Display current info in a clean format
st.header("Account Information")
st.write(f"**Name:** {st.session_state.get('first_name', '')} {st.session_state.get('last_name', '')}")
st.write(f"**Email:** {st.session_state.get('email', '')}")
st.write(f"**Member Since:** {st.session_state.get('member_since', 'N/A')}")

st.header("Business Details")
st.write(f"**Business Name:** {st.session_state.get('business_name', 'Not provided')}")
st.write(f"**Contact Phone:** {st.session_state.get('phone', 'Not provided')}")

# Single edit button that shows form when clicked
if st.button("Edit Profile"):
    with st.form("edit_form"):
        new_phone = st.text_input("Phone", value=st.session_state.get('phone', ''))
        new_business = st.text_input("Business Name", value=st.session_state.get('business_name', ''))
        
        if st.form_submit_button("Save"):
            st.session_state['phone'] = new_phone
            st.session_state['business_name'] = new_business
            st.success("Profile updated")
            st.rerun()