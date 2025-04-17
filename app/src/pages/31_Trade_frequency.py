import streamlit as st
import pandas as pd
import requests
import altair as alt
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()
st.title("Trade Frequency Over Time")

API_BASE = "http://api:4000"


try:
    response = requests.get(f"{API_BASE}/analytics/trade-frequency")
    data = response.json()
    df = pd.DataFrame(data, format='ISO8601')

    if not df.empty:
        df['trade_date'] = pd.to_datetime(df['trade_date'])
        chart = alt.Chart(df).mark_line(point=True).encode(
            x='trade_date:T',
            y='num_trades:Q'
        ).properties(
            width=800,
            height=400,
            title="Number of Trades Per Day"
        )
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("No trade data available.")
except Exception as e:
    st.error(f"Error fetching data: {e}")
