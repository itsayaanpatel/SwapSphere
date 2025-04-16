import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()
st.title("📤 Export Trade Summary Report")

API_BASE = "http://localhost:5000/api"

try:
    response = requests.get(f"{API_BASE}/analytics/export-summary")
    summary = response.json()

    st.subheader("📊 Summary Metrics")
    st.metric("Total Trades", summary.get("total_trades", 0))
    st.metric("Avg. Fairness Score", summary.get("average_fairness_score", "N/A"))
    st.metric("Total Fraud Reports", summary.get("total_fraud_reports", 0))

    st.divider()
    st.download_button(
        label="Download Summary Report (JSON)",
        data=str(summary),
        file_name="trade_summary_report.json",
        mime="application/json"
    )
except Exception as e:
    st.error(f"Error fetching summary data: {e}")
