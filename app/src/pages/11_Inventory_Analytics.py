import streamlit as st
import requests
import pandas as pd
import plotly.express as px

def show():
    st.title("📊 Inventory Analytics")
    st.markdown("Performance metrics for your listings")
    
    # Date range selector
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=pd.to_datetime("2024-01-01"))
    with col2:
        end_date = st.date_input("End Date", value=pd.to_datetime("today"))
    
    # Fetch seller analytics
    data = requests.get(
        "http://api:5000/api/analytics/seller",
        params={
            "seller_id": st.session_state.user_id,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        }
    ).json()
    
    # Section 1: Key Metrics
    st.subheader("📈 Performance Summary")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Total Listings", data["summary"]["total_listings"])
    kpi2.metric("Avg. Time to Sell", f"{data['summary']['avg_days_to_sell']} days")
    kpi3.metric("Conversion Rate", f"{data['summary']['conversion_rate']}%")
    kpi4.metric("Total Revenue", f"${data['summary']['total_revenue']:,.2f}")
    
    # Section 2: Category Breakdown
    st.subheader("🛍️ By Category")
    df_category = pd.DataFrame(data["by_category"])
    fig1 = px.pie(
        df_category,
        names="category",
        values="items_sold",
        hole=0.3,
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    # Section 3: Price Distribution
    st.subheader("💵 Price Performance")
    df_prices = pd.DataFrame(data["price_distribution"])
    fig2 = px.box(
        df_prices,
        x="category",
        y="sale_price",
        points="all",
        color="category"
    )
    st.plotly_chart(fig2, use_container_width=True)
    
    # Section 4: Raw Data
    with st.expander("📝 View Raw Data"):
        st.dataframe(
            pd.DataFrame(data["raw_data"]),
            column_config={
                "sold_date": "Date Sold",
                "item_name": "Item",
                "sale_price": st.column_config.NumberColumn(
                    "Price",
                    format="$%.2f"
                ),
                "days_to_sell": "Days Listed"
            },
            hide_index=True
        )
    
    # Auto-refresh every 5 minutes
    st.cache_data(ttl=300)