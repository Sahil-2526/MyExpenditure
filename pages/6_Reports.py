import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from database import Database
from finance_manager import FinanceManager
from enums import TransactionType

st.set_page_config(page_title="Reports - MyExpenditure", page_icon="📈", layout="wide")

def render_reports():
    st.title("📈 Analytics & Reports Dashboard")
    st.markdown("Comprehensive financial reporting, trend visualizations, and analytics.")
    st.markdown("---")

    db = Database()
    manager = FinanceManager(db)

    try:
        transactions = manager.get_all_transactions()
        categories = manager.get_all_categories()
        cat_map = {c[0]: c[1] for c in categories}
        
        # Calculate totals safely from tuples
        total_income = sum(t[1] for t in transactions if t[3] == TransactionType.CREDIT.value)
        total_expense = sum(t[1] for t in transactions if t[3] == TransactionType.DEBIT.value)
        total_savings = total_income - total_expense
        
        cat_spending = {}
        for t in transactions:
            if t[3] == TransactionType.DEBIT.value:
                cat_name = cat_map.get(t[4], "Uncategorized")
                cat_spending[cat_name] = cat_spending.get(cat_name, 0.0) + t[1]
                
    except Exception as e:
        st.error(f"Error loading reports data: {e}")
        transactions = []
        total_income, total_expense, total_savings = 0.0, 0.0, 0.0
        cat_spending = {}
    finally:
        db.close()

    if not transactions:
        st.info("No transaction data available to generate reports.")
        return

    df = pd.DataFrame(transactions, columns=['id', 'amount', 'date', 'transaction_type', 'category_id', 'note'])

    st.subheader("Financial Summary Metrics")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Credit (Income)", f"₹{total_income:,.2f}")
    c2.metric("Total Debit (Expense)", f"₹{total_expense:,.2f}")
    c3.metric("Net Savings (Balance)", f"₹{total_savings:,.2f}")

    st.markdown("---")

    # Analytics Visualizations
    st.subheader("Visual Analytics")
    col_r1, col_r2 = st.columns(2)

    with col_r1:
        st.markdown("#### Category-Wise Spending (Pie Chart)")
        if cat_spending:
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.pie(list(cat_spending.values()), labels=list(cat_spending.keys()), autopct='%1.1f%%', startangle=140, colors=plt.cm.Pastel1.colors)
            ax.axis('equal')
            st.pyplot(fig)
        else:
            st.info("Insufficient expense data for pie chart.")

    with col_r2:
        st.markdown("#### Credit vs Debit Comparison (Bar Chart)")
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(['Total Credit', 'Total Debit'], [total_income, total_expense], color=['#27ae60', '#c0392b'])
        ax.set_ylabel("Amount (₹)")
        st.pyplot(fig)

    st.markdown("---")

    # CSV Download Section
    st.subheader("Download Reports")
    csv_report = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Full Financial Report as CSV",
        data=csv_report,
        file_name="financial_report.csv",
        mime="text/csv"
    )

if __name__ == "__main__":
    render_reports()