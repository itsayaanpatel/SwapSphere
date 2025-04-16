"""
24_User_Management.py

This page allows the System Administrator to view and manage platform users.
It fetches all users via GET /users, then for each user displays:
  - user_id, username, email, trust_score
  - a button to “Ban” (set trust_score=0) or “Unban” (restore trust_score to 100)
  
Clicking the button sends a PUT to /users/<user_id> with the new trust_score.
"""

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()

st.title("User Management")

# 1) Fetch all users
try:
    resp = requests.get("http://api:4000/users")
    resp.raise_for_status()
    users = resp.json()
except Exception as e:
    st.error(f"Failed to fetch users: {e}")
    st.stop()

# 2) Display in a table-like layout
for u in users:
    col1, col2, col3, col4, col5 = st.columns([1, 2, 3, 1, 2])
    with col1:
        st.write(u["user_id"])
    with col2:
        st.write(u["username"])
    with col3:
        st.write(u["email"])
    with col4:
        st.write(f"{u['trust_score']:.1f}")
    with col5:
        # Decide label based on current trust_score
        if u["trust_score"] > 0:
            action_label = "Ban"
            new_score = 0
        else:
            action_label = "Unban"
            new_score = 100
        if st.button(action_label, key=f"user_{u['user_id']}"):
            try:
                update = {"trust_score": new_score}
                upd_resp = requests.put(f"http://api:4000/users/{u['user_id']}", json=update)
                upd_resp.raise_for_status()
                st.success(f"{action_label}ned user {u['username']} (ID {u['user_id']})")
                st.experimental_rerun()
            except Exception as ex:
                st.error(f"Failed to {action_label.lower()} user: {ex}")

# 3) Add a legend/header row
st.markdown("---")
st.markdown("**Columns:** ID | Username | Email | Trust Score | Action") 
