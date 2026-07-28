import streamlit as st
from database import Database

# Page Configuration
st.set_page_config(
    page_title="MyExpenditure - Personal Finance Manager",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # Initialize database tables on startup
    # Sidebar Header & Navigation Menu
    with st.sidebar:
        st.title("MyExpenditure")
        st.markdown("---")

    db = Database()
    db.create_tables()
    db.close()

    # Define pages explicitly with Dashboard as the default first page
    dashboard_page = st.Page("pages/1_Dashboard.py", title="Dashboard", icon="📊", default=True)
    transactions_page = st.Page("pages/2_Transactions.py", title="Transactions", icon="💳")
    categories_page = st.Page("pages/3_Categories.py", title="Categories", icon="📁")
    budgets_page = st.Page("pages/4_Budgets.py", title="Budgets", icon="🎯")
    goals_page = st.Page("pages/5_Goals.py", title="Goals", icon="🏆")
    reports_page = st.Page("pages/6_Reports.py", title="Reports", icon="📈")

    # Set up navigation structure
    pg = st.navigation({
        "Overview": [dashboard_page],
        "Management": [transactions_page, categories_page, budgets_page, goals_page],
        "Analytics": [reports_page]
    })

    # Run the selected page
    pg.run()

if __name__ == "__main__":
    main()