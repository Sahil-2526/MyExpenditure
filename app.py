import streamlit as st
from database import Database
from pages.auth import render_auth

# Page Configuration
st.set_page_config(
    page_title="MyExpenditure - Personal Finance Manager",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # Initialize database tables on startup
    db = Database()
    db.create_tables()
    db.close()

    # Check if user is authenticated in session state
    if 'uid' not in st.session_state or st.session_state.uid == None:
        st.session_state.uid = None
        render_auth()
        return

    # --- LOGGED IN EXPERIENCE ---
    
    # Define multi-page setup
    dashboard_page = st.Page("pages/1_Dashboard.py", title="Dashboard", icon="📊", default=True)
    transactions_page = st.Page("pages/2_Transactions.py", title="Transactions", icon="💳")
    categories_page = st.Page("pages/3_Categories.py", title="Categories", icon="📁")
    budgets_page = st.Page("pages/4_Budgets.py", title="Budgets", icon="🎯")
    goals_page = st.Page("pages/5_Goals.py", title="Goals", icon="🏆")
    reports_page = st.Page("pages/6_Reports.py", title="Reports", icon="📈")

    # Sidebar Header
    with st.sidebar:
        st.markdown("## 💰 MyExpenditure")
        if "username" in st.session_state:
            st.caption(f"Logged in as: **{st.session_state.username}** (UID: {st.session_state.uid})")
        st.markdown("---")

    # Navigation menu
    pg = st.navigation([
        dashboard_page,
        transactions_page,
        categories_page,
        budgets_page,
        goals_page,
        reports_page
    ])

    # Sidebar Footer & Logout Mechanism
    with st.sidebar:
        st.markdown("---")
        if st.button("🚪 Log Out", use_container_width=True):
            st.session_state.uid = None
            st.session_state.username = None
            st.rerun()

        st.markdown("#### 🗄️ Database Status")
        st.success("Connected to SQLite Database")
        st.markdown("---")
        st.markdown("#### 🎨 Theme Information")
        st.info("Active Theme: Dark / Shadow & Silk")

    # Run selected page
    pg.run()

if __name__ == "__main__":
    main()