"""
22_Fraud_Reports.py

System Administrator page for reviewing and managing fraud reports.

Features:
  - Fetch and list all fraud reports via GET /fraud_reports
  - For each report, show reporter, trade_id, reason, status
  - Allow admin to update status (Under Review, Resolved, Dismissed) via PUT /fraud_reports/<report_id>
"""

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()

st.title("Fraud Reports Management")

# Fetch fraud reports
try:
    resp = requests.get("http://localhost:4000/fraud_reports")
    resp.raise_for_status()
    reports = resp.json()
except Exception as e:
    st.error(f"Failed to fetch fraud reports: {e}")
    st.stop()

# Display each report in an expander
for rep in reports:
    header = f"Report #{rep['report_id']} (Status: {rep['status']})"
    with st.expander(header, expanded=False):
        st.write(f"**Reporter ID:** {rep['reported_by']}")
        st.write(f"**Trade ID:** {rep['trade_id']}")
        st.write(f"**Reason:** {rep['reason']}")
        st.write(f"**Reported On:** {rep.get('created_at', 'N/A')}  ")

        col1, col2, col3 = st.columns(3)
        # Mark as Resolved
        with col1:
            if st.button("Resolve", key=f"resolve_{rep['report_id']}"):
                try:
                    update = {"status": "Resolved"}
                    put = requests.put(f"http://localhost:4000/fraud_reports/{rep['report_id']}", json=update)
                    put.raise_for_status()
                    st.success("Report marked Resolved.")
                    st.experimental_rerun()
                except Exception as ex:
                    st.error(f"Failed to resolve: {ex}")
        # Dismiss report
        with col2:
            if st.button("Dismiss", key=f"dismiss_{rep['report_id']}"):
                try:
                    update = {"status": "Dismissed"}
                    put = requests.put(f"http://localhost:4000/fraud_reports/{rep['report_id']}", json=update)
                    put.raise_for_status()
                    st.success("Report Dismissed.")
                    st.experimental_rerun()
                except Exception as ex:
                    st.error(f"Failed to dismiss: {ex}")
        # Re-open as Under Review
        with col3:
            if st.button("Reopen", key=f"reopen_{rep['report_id']}"):
                try:
                    update = {"status": "Under Review"}
                    put = requests.put(f"http://localhost:4000/fraud_reports/{rep['report_id']}", json=update)
                    put.raise_for_status()
                    st.success("Report reopened for review.")
                    st.experimental_rerun()
                except Exception as ex:
                    st.error(f"Failed to reopen: {ex}")
#end
