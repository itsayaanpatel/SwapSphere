import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title('Negotiate Deal')

trade_id = st.text_input("Enter Trade ID")

if trade_id:
    # Fetch current trade details
    response = requests.get(f"http://localhost:4000/negotiate_deal/{trade_id}")
    if response.status_code == 200:
        trade = response.json()
        st.write("Current Trade Details:")
        st.dataframe(trade)

        new_cash_adjustment = st.number_input("Propose Cash Adjustment", step=1)

        if st.button("Submit Cash Proposal", type="primary"):
            update_response = requests.put(
                f"http://localhost:4000/negotiate_deal/{trade_id}",
                json={"cash_adjustment": new_cash_adjustment}
            )
            if update_response.status_code == 200:
                st.success("Cash adjustment proposal submitted successfully!")
            else:
                st.error("Failed to submit proposal.")
    else:
        st.error("Failed to fetch trade details.")
