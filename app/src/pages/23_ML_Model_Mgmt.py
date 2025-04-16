"""
23_ML_Model_Mgmt.py

Admin page for ML Model 01 management:
  - Train Model 01 (POST /c/train)
  - Test Model 01 (POST /c/test)
  - Predict with Model 01 (GET /c/prediction/<var1>/<var2>)
"""

import streamlit as st
import requests
from modules.nav import SideBarLinks

# Page configuration and sidebar navigation
st.set_page_config(layout="wide")
SideBarLinks()

# Title and description
st.title("ML Model Management")
st.write("Use this page to train, test, and make predictions with Model 01.")

# --- Train Model 01 ---
if st.button("Train Model 01", type="primary", use_container_width=True):
    try:
        response = requests.post("http://api:4000/c/train")
        response.raise_for_status()
        st.success(f"Training successful: {response.text}")
    except Exception as e:
        st.error(f"Training failed: {e}")

# --- Test Model 01 ---
if st.button("Test Model 01", type="secondary", use_container_width=True):
    try:
        response = requests.post("http://api:4000/c/test")
        response.raise_for_status()
        st.success(f"Test successful: {response.text}")
    except Exception as e:
        st.error(f"Test failed: {e}")

# --- Prediction Section ---
st.subheader("Make a Prediction with Model 01")
with st.form("prediction_form"):
    var1 = st.number_input("Variable 01:", step=1, format="%i")
    var2 = st.number_input("Variable 02:", step=1, format="%i")
    if st.form_submit_button("Get Prediction"):
        try:
            pred_resp = requests.get(f"http://api:4000/c/prediction/{var1}/{var2}")
            pred_resp.raise_for_status()
            result = pred_resp.json().get("result")
            st.metric("Predicted Value", f"{result}")
        except Exception as e:
            st.error(f"Prediction failed: {e}")
