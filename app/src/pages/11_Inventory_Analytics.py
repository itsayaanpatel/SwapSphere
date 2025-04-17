import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from modules.nav import SideBarLinks
from datetime import datetime

# ------------------------------------------------------
# Page configuration & nav
# ------------------------------------------------------
st.set_page_config(layout="wide")
SideBarLinks()

st.title("📊 Inventory Analytics")
st.markdown("Performance metrics for your listings")

# ------------------------------------------------------
# 1 – Identify the seller (prompt when missing)
# ------------------------------------------------------
seller_id = st.session_state.get("user_id")
if not seller_id:
    seller_id = st.text_input("Enter your Seller ID:")

if not seller_id:
    st.info("Please provide your Seller ID to load analytics.")
    st.stop()

# ------------------------------------------------------
# 2 – Date range picker (not used by back‑end yet, but we keep it
#     for future compatibility)
# ------------------------------------------------------
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", value=pd.to_datetime("2024-01-01"))
with col2:
    end_date = st.date_input("End Date", value=pd.to_datetime("today"))

# ------------------------------------------------------
# 3 – Fetch raw item data for this seller (cached 5 min)
# ------------------------------------------------------
@st.cache_data(ttl=300, show_spinner="Fetching inventory …")
def fetch_items(_seller_id: str):
    """Returns a list[dict] of this seller's items from the API."""
    # NOTE: the current Flask route ignores query params; it lists *all* items
    #       so we fall back to the per‑seller route if it exists, else filter
    
    endpoints = [
        f"http://api:4000/seller/items?seller_id={_seller_id}",   # hoped‑for route
        f"http://api:4000/seller/items/user/{_seller_id}"          # fallback route in item_routes.py
    ]
    for url in endpoints:
        try:
            r = requests.get(url, timeout=10)
            if r.ok:
                data = r.json()
                if isinstance(data, list):
                    # filter client‑side just in case we got everything
                    return [d for d in data if str(d.get("user_id")) == str(_seller_id)] or data
        except Exception:
            continue
    return []

items = fetch_items(seller_id)
if not items:
    st.warning("No items found for this seller.")
    st.stop()

# Make DataFrame for easier manipulation
DF = pd.DataFrame(items)

# ------------------------------------------------------
# 4 – Compute simple metrics from the data we actually have
# ------------------------------------------------------
TOTAL_LISTINGS = len(DF)

# Conversion rate (items marked Sold / total)
if "status" in DF.columns:
    sold_mask = DF["status"].str.lower() == "sold"
    SOLD_COUNT = sold_mask.sum()
    CONVERSION_RATE = round(SOLD_COUNT / TOTAL_LISTINGS * 100, 2)
else:
    CONVERSION_RATE = "—"

# Average days to sell (needs created_at & sold_date)
if set(["created_at", "sold_date"]).issubset(DF.columns):
    def _to_dt(x):
        return pd.to_datetime(x, errors="coerce")
    delta = (_to_dt(DF["sold_date"]) - _to_dt(DF["created_at"]))
    AVG_DAYS = round(delta.dt.days.mean(), 1)
    AVG_DAYS = AVG_DAYS if pd.notna(AVG_DAYS) else "—"
else:
    AVG_DAYS = "—"

# Total revenue (sum of sale_price if present, else 0)
if "sale_price" in DF.columns:
    TOTAL_REVENUE = DF["sale_price"].fillna(0).sum()
else:
    TOTAL_REVENUE = 0

# ------------------------------------------------------
# 5 – Render KPI deck
# ------------------------------------------------------
st.subheader("📈 Performance Summary")
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Listings", TOTAL_LISTINGS)
k2.metric("Avg. Time to Sell", f"{AVG_DAYS} days" if AVG_DAYS != "—" else "—")
k3.metric("Conversion Rate", f"{CONVERSION_RATE}%" if CONVERSION_RATE != "—" else "—")
k4.metric("Total Revenue", f"${TOTAL_REVENUE:,.2f}")

# ------------------------------------------------------
# 6 – Category breakdown (pie) – requires 'category'
# ------------------------------------------------------
if "category" in DF.columns:
    st.subheader("🛍️ By Category")
    cat_counts = (
        DF.groupby("category", dropna=False)
          .size()
          .reset_index(name="count")
    )
    fig_cat = px.pie(cat_counts, names="category", values="count", hole=0.3)
    st.plotly_chart(fig_cat, use_container_width=True)

# ------------------------------------------------------
# 7 – Price distribution (box) – prefer sale_price else estimated_value
# ------------------------------------------------------
PRICE_COL = "sale_price" if "sale_price" in DF.columns else "estimated_value"
if PRICE_COL in DF.columns:
    st.subheader("💵 Price Distribution")
    fig_price = px.box(DF, x="category" if "category" in DF.columns else PRICE_COL,
                       y=PRICE_COL, points="all", color="category" if "category" in DF.columns else None)
    st.plotly_chart(fig_price, use_container_width=True)

# ------------------------------------------------------
# 8 – Raw data expander
# ------------------------------------------------------
with st.expander("📝 View Raw Data"):
    st.dataframe(DF, hide_index=True)
