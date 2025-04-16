"""
21_System_Dashboard.py

System Administrator dashboard overview:
  - Key platform metrics (total users, total trades, average trades per day)
  - Trade frequency chart (analytics/trends)
  - Fraud pattern chart (analytics/fraud)
  - Recent system logs (logs)
"""

import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()

st.title("System Dashboard")
st.write("Overview of platform health and activity. Metrics below:")

# --- Fetch Data ---
with st.spinner("Loading metrics..."):
    # Total users
    try:
        users_resp = requests.get("http://api:4000/users")
        users_resp.raise_for_status()
        total_users = len(users_resp.json())
    except Exception:
        total_users = "n/a"

    # Total trades
    try:
        trades_resp = requests.get("http://api:4000/trades/count")
        trades_resp.raise_for_status()
        total_trades = trades_resp.json().get("count", "n/a")
    except Exception:
        total_trades = "n/a"

    # Avg trades per day (if available)
    try:
        avg_resp = requests.get("http://api:4000/trades/average_daily")
        avg_resp.raise_for_status()
        avg_daily = avg_resp.json().get("average", "n/a")
    except Exception:
        avg_daily = "n/a"

    # Recent logs
    try:
        logs_resp = requests.get("http://api:4000/logs")
        logs_resp.raise_for_status()
        df_logs = pd.DataFrame(logs_resp.json())
    except Exception:
        df_logs = pd.DataFrame()

# --- Display Metrics ---
st.subheader("📊 Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Users", total_users)
col2.metric("Total Trades", total_trades)
col3.metric("Avg Trades/Day", avg_daily)

# --- Recent System Logs ---
st.subheader("📝 Recent System Logs")
if not df_logs.empty:
    df_recent = df_logs.sort_values('log_time', ascending=False).head(10)
    st.dataframe(df_recent, use_container_width=True)
else:
    st.write("No logs available.")

