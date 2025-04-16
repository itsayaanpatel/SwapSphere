import streamlit as st
import pandas as pd
import requests
import altair as alt
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()
st.title("Top Traded Item Categories")

API_BASE = "http://api:5000/api"

try:
    response = requests.get(f"{API_BASE}/analytics/top-categories")
    data = response.json()
    df = pd.DataFrame(data)

    if not df.empty:
        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X('times_traded:Q', title='Times Traded'),
            y=alt.Y('category:N', sort='-x', title='Item Category')
        ).properties(
            width=700,
            height=400,
            title="Most Frequently Traded Categories"
        )
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("No category trade data available.")
except Exception as e:
    st.error(f"Error fetching data: {e}")
