import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from database import Database
from finance_manager import FinanceManager
from enums import TransactionType

st.set_page_config(page_title="Dashboard - MyExpenditure", page_icon="📊", layout="wide")

def render_dashboard():
    st.title("📊 Financial Dashboard")
    st.markdown("Get a high-level overview of your financial status, active limits, and recent activity.")
    st.markdown("---")

    db = Database()
    manager = FinanceManager(db)

    try:
        transactions = manager.get_all_transactions()
        categories = manager.get_all_categories()
        cat_map = {c[0]: c[1] for c in categories}
        budgets = manager.get_all_budgets()
        goals = manager.get_all_goals()
        
        # Calculate totals from tuples: index 1 is amount, index 3 is transaction_type, index 4 is category_id
        total_income = sum(t[1] for t in transactions if t[3] == TransactionType.CREDIT.value)
        total_expense = sum(t[1] for t in transactions if t[3] == TransactionType.DEBIT.value)
        current_balance = total_income - total_expense
        
        # Calculate category wise spending from tuples
        cat_spending = {}
        for t in transactions:
            if t[3] == TransactionType.DEBIT.value:
                cat_name = cat_map.get(t[4], "Uncategorized")
                cat_spending[cat_name] = cat_spending.get(cat_name, 0.0) + t[1]
                
    except Exception as e:
        st.error(f"Error loading data from backend: {e}")
        transactions, categories, budgets, goals = [], [], [], []
        total_income, total_expense, current_balance, cat_spending = 0.0, 0.0, 0.0, {}
    finally:
        db.close()

    savings = current_balance
    num_transactions = len(transactions)
    num_categories = len(categories)
    active_budgets = len(budgets)
    active_goals = len(goals)

    # Top Metric Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Current Balance", value=f"₹{current_balance:,.2f}")
    with col2:
        st.metric(label="Total Income (Credit)", value=f"₹{total_income:,.2f}")
    with col3:
        st.metric(label="Total Expense (Debit)", value=f"₹{total_expense:,.2f}")
    with col4:
        st.metric(label="Net Savings", value=f"₹{savings:,.2f}")

    st.markdown("")
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        st.metric(label="Transactions", value=num_transactions)
    with col6:
        st.metric(label="Categories", value=num_categories)
    with col7:
        st.metric(label="Active Budgets", value=active_budgets)
    with col8:
        st.metric(label="Active Goals", value=active_goals)

    st.markdown("---")

    # Additional Quick Stats & Insights
    c1, c2, c3 = st.columns(3)
    top_spending_category = max(cat_spending, key=cat_spending.get) if cat_spending else "N/A"

    with c1:
        st.info(f"**Total Transactions Recorded:** {num_transactions}")
    with c2:
        st.success(f"**Account Health:** Stable")
    with c3:
        st.warning(f"**Top Spending Category:** {top_spending_category}")

    st.markdown("---")

    # Recent Transactions & Budget Overview
    col_tab1, col_tab2 = st.columns(2)
    
    with col_tab1:
        st.subheader("Recent Transactions")
        if transactions:
            st.dataframe(pd.DataFrame(transactions[:5], columns=['ID', 'Amount', 'Date', 'Type', 'Category ID', 'Note']), use_container_width=True)
        else:
            st.info("No recent transactions found.")

    with col_tab2:
        st.subheader("Active Budgets Overview")
        if budgets:
            for b in budgets:
                st.text(f"Budget ID {b[0]} | Limit: ₹{b[2]} | Month/Year: {b[3]}/{b[4]}")
        else:
            st.info("No active budgets configured.")

if __name__ == "__main__":
    render_dashboard()