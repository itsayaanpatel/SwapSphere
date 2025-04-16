"""
04_Buyer_Profile.py

Simple profile page for buyers to view and manage their account information.
"""

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Display buyer-specific sidebar links
SideBarLinks()

st.title(f"Your Profile, {st.session_state.get('first_name', 'Buyer')}")
st.divider()

# Profile display section
col1, col2 = st.columns(2)

with col1:
    st.subheader("Account Details")
    st.write(f"**Name:** {st.session_state.get('first_name', '')} {st.session_state.get('last_name', '')}")
    st.write(f"**Email:** {st.session_state.get('email', '')}")
    st.write(f"**Member Since:** {st.session_state.get('member_since', 'N/A')}")

with col2:
    st.subheader("Preferences")
    st.write(f"**Preferred Contact Method:** {st.session_state.get('contact_preference', 'Email')}")
    st.write(f"**Trade Radius:** {st.session_state.get('trade_radius', '100')} miles")

st.divider()

# Minimal edit form
with st.expander("Update Preferences"):
    with st.form("buyer_profile_form"):
        contact_pref = st.selectbox(
            "Contact Preference",
            ["Email", "Phone", "Text"],
            index=["Email", "Phone", "Text"].index(st.session_state.get('contact_preference', 'Email'))
        )
        trade_radius = st.slider(
            "Maximum Trade Distance (miles)",
            10, 500,
            value=int(st.session_state.get('trade_radius', 100))
        
        if st.form_submit_button("Save Preferences"):
            st.session_state['contact_preference'] = contact_pref
            st.session_state['trade_radius'] = str(trade_radius)
            st.success("Preferences updated!")
            st.rerun()