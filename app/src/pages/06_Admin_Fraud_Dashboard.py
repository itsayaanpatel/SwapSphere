# pages/21_Admin_Fraud.py
import streamlit as st
from modules.nav import SideBarLinks
from backend.db_connection import db
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
SideBarLinks()

# --- Database Functions ---
def get_fraud_reports():
    with db.cursor(dictionary=True) as cursor:
        cursor.execute("""
            SELECT fr.*, 
                   u1.username as reporter_name,
                   u2.username as reported_name,
                   t.status as trade_status
            FROM Fraud_Reports fr
            JOIN Users u1 ON fr.reported_by = u1.user_id
            JOIN Trades t ON fr.trade_id = t.trade_id
            JOIN Users u2 ON t.proposer_id = u2.user_id OR t.receiver_id = u2.user_id
            WHERE fr.status = 'Under Review'
            ORDER BY fr.created_at DESC
        """)
        return cursor.fetchall()

def get_suspicious_users():
    with db.cursor(dictionary=True) as cursor:
        cursor.execute("""
            SELECT u.user_id, u.username, u.trust_score,
                   COUNT(fr.report_id) as report_count
            FROM Users u
            LEFT JOIN Fraud_Reports fr ON u.user_id = fr.reported_by
            GROUP BY u.user_id
            HAVING report_count > 0
            ORDER BY report_count DESC
            LIMIT 10
        """)
        return cursor.fetchall()

# --- UI Components ---
def display_fraud_metrics():
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Pending Investigations", "12", "+3 this week")
    with col2:
        st.metric("Confirmed Fraud Cases", "4", "-1 from last week")
    with col3:
        st.metric("Average Resolution Time", "2.1 days")

def display_fraud_patterns():
    with db.cursor() as cursor:
        cursor.execute("""
            SELECT reason, COUNT(*) as count
            FROM Fraud_Reports
            WHERE status = 'Resolved'
            GROUP BY reason
        """)
        data = cursor.fetchall()
    
    df = pd.DataFrame(data, columns=["Reason", "Count"])
    fig = px.pie(df, values='Count', names='Reason', 
                 title='Common Fraud Patterns')
    st.plotly_chart(fig, use_container_width=True)

# --- Main UI ---
st.title("Fraud Monitoring Dashboard")

if st.session_state.get('role') != 'admin':
    st.error("Admin access required")
    st.stop()

# --- Layout ---
display_fraud_metrics()

tab1, tab2, tab3 = st.tabs(["Pending Cases", "User Risk Analysis", "Patterns"])

with tab1:
    st.subheader("Flagged Transactions")
    reports = get_fraud_reports()
    
    for report in reports:
        with st.expander(f"Case #{report['report_id']} - {report['reason'][:30]}..."):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Reporter:** {report['reporter_name']}")
                st.write(f"**Reported User:** {report['reported_name']}")
                st.write(f"**Trade Status:** {report['trade_status']}")
            with col2:
                st.write(f"**Date:** {report['created_at'].strftime('%Y-%m-%d')}")
                st.write(f"**Details:** {report['reason']}")
            
            st.text_area("Investigation Notes", key=f"notes_{report['report_id']}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("Dismiss", key=f"dismiss_{report['report_id']}"):
                    # Update status to Dismissed
                    pass
            with col2:
                if st.button("Mark as Fraud", key=f"fraud_{report['report_id']}"):
                    # Update status and adjust trust scores
                    pass
            with col3:
                if st.button("Request More Info", key=f"info_{report['report_id']}"):
                    # Send notification to reporter
                    pass

with tab2:
    st.subheader("High-Risk Users")
    users = get_suspicious_users()
    df = pd.DataFrame(users)
    st.dataframe(
        df,
        column_config={
            "user_id": "User ID",
            "username": "Username",
            "trust_score": st.column_config.ProgressColumn(
                "Trust Score",
                format="%f",
                min_value=0,
                max_value=100
            ),
            "report_count": "Fraud Reports"
        },
        hide_index=True,
        use_container_width=True
    )

with tab3:
    display_fraud_patterns()
    st.subheader("Recent Fraud Patterns")
    st.write("""
    - **Counterfeit Items**: 42% of cases
    - **Shipping Scams**: 28% of cases  
    - **Payment Avoidance**: 18% of cases
    - **Account Takeover**: 12% of cases
    """)