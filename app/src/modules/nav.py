# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

import streamlit as st

#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")

def AboutPageNav():
    st.sidebar.page_link("pages/40_About.py", label="About", icon="🧠")


#### ------------------------ For Buyer Role ------------------------
def BuyerHomeNav():
    st.sidebar.page_link("pages/00_Buyer_Home.py", label="Buyer Home", icon="🛍️")

def TradeMatchingNav():
    st.sidebar.page_link("pages/01_Trade_Matching.py", label="Trade Matching", icon="🔍")

def MarketValuationsNav():
    st.sidebar.page_link("pages/02_Market_Valuations.py", label="Market Valuations", icon="💲")

def NegotiateDealNav():
    st.sidebar.page_link("pages/03_Negotiate_Deal.py", label="Negotiate Deal", icon="🤝")

def BuyerProfileNav():
    st.sidebar.page_link("pages/05_Buyer_Profile.py", label="Buyer Profile", icon="👤") #This shared #05 with Trade_Negotiation so I left it as is

def TradeNegotiationNav():
    st.sidebar.page_link("pages/05_Trade_Negotiation.py", label="Trade Negotiation", icon="💬")


#### ------------------------ For Seller Role ------------------------
def SellerHomeNav():
    st.sidebar.page_link("pages/10_Seller_Home.py", label="Seller Home", icon="🛒")

def InventoryAnalyticsNav():
    st.sidebar.page_link("pages/11_Inventory_Analytics.py", label="Inventory Analytics", icon="📊")

def SellerProfileNav():
    st.sidebar.page_link("pages/12_Seller_Profile.py", label="Seller Profile", icon="👤")

def UploadItemsNav():
    st.sidebar.page_link("pages/13_Upload_Items.py", label="Upload New Items", icon="➕")

def TradeHistoryNav():
    st.sidebar.page_link("pages/14_Trade_History.py", label="Trade History", icon="📜")

def ManageListingsNav():
    st.sidebar.page_link("pages/15_Manage_Listings.py", label="Manage Listings", icon="🛠️")

#### ------------------------ For System Admin Role ------------------------
def AdminHomeNav():
    st.sidebar.page_link("pages/20_Admin_Home.py", label="Admin Home", icon="🖥️")

#Placeholder for whatever page we decide to use here
#def FraudDashboardNav():
   # st.sidebar.page_link("pages/06_Admin_Fraud_Dashboard.py", label="Fraud Dashboard", icon="🚨")

#Not sure if we will do the same thing as was done in the template so I commented this out
#def MLModelNav():
  #  st.sidebar.page_link("pages/21_ML_Model_Mgmt.py", label="ML Model Management", icon="🏢")

def UserManagementNav():
    # If you add a user management page, uncomment or add here:
    # st.sidebar.page_link("pages/24_User_Management.py", label="User Management", icon="👥")
    pass


#### ------------------------ For Data Analyst Role ------------------------
def DataAnalystHomeNav():
    st.sidebar.page_link("pages/30_Data_Analyst_Home.py", label="Data Analyst Home", icon="📊")


# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    Adds navigation links to the sidebar based on the logged-in user's role,
    which is stored in st.session_state.
    
    The links include:
      - A Home link if show_home is True.
      - Role-specific links for Buyer, Seller, System Admin, and Data Analyst.
      - The About page link.
      - A Logout button if the user is authenticated.
    """
    st.sidebar.image("assets/logo.png", width=150)

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        HomeNav()

    if st.session_state["authenticated"]:
        role = st.session_state.get("role")
        if role == "buyer":
            BuyerHomeNav()
            TradeMatchingNav()
            MarketValuationsNav()
            NegotiateDealNav()
            BuyerProfileNav()
            TradeNegotiationNav()
        elif role == "seller":
            SellerHomeNav()
            UploadItemsNav()
            TradeHistoryNav()
            ManageListingsNav()
            InventoryAnalyticsNav()
            SellerProfileNav()
        elif role == "administrator":
            AdminHomeNav()
            #FraudDashboardNav() see comments above under admin
            #MLModelNav() see comments above under admin
            UserManagementNav()
        elif role == "data_analyst":
            DataAnalystHomeNav()
        # You may add additional roles here when the pages are done

    AboutPageNav()

    if st.session_state["authenticated"]:
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")
