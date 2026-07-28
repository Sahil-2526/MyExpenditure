import streamlit as st
import pandas as pd
from datetime import datetime
from database import Database
from finance_manager import FinanceManager
from transaction import Transaction
from enums import TransactionType

st.set_page_config(page_title="Transactions - MyExpenditure", page_icon="💳", layout="wide")

def render_transactions():
    st.title("💳 Transaction Management")
    st.markdown("Add, edit, filter, search, and manage your financial inflows and outflows.")
    st.markdown("---")

    db = Database()
    manager = FinanceManager(db)

    try:
        transactions = manager.get_all_transactions()
        categories = manager.get_all_categories()
        cat_map = {c[0]: c[1] for c in categories} # id -> name mapping
        
        # Calculate totals safely from raw database tuples
        total_credit = sum(t[1] for t in transactions if t[3] == TransactionType.CREDIT.value)
        total_debit = sum(t[1] for t in transactions if t[3] == TransactionType.DEBIT.value)
    except Exception as e:
        st.error(f"Error fetching backend data: {e}")
        transactions, categories, cat_map = [], [], {}
        total_credit, total_debit = 0.0, 0.0

    df = pd.DataFrame(transactions, columns=['id', 'amount', 'date', 'transaction_type', 'category_id', 'note']) if transactions else pd.DataFrame(columns=['id', 'amount', 'date', 'transaction_type', 'category_id', 'note'])

    tab1, tab2, tab3 = st.tabs(["View & Filter Transactions", "Add Transaction", "Manage / Delete"])

    with tab1:
        st.subheader("All Transactions")
        if not df.empty:
            df['Category Name'] = df['category_id'].map(cat_map)
            st.dataframe(df[['id', 'date', 'amount', 'transaction_type', 'Category Name', 'note']], use_container_width=True)
            
            c1, c2 = st.columns(2)
            c1.metric("Total Credits", f"₹{total_credit:,.2f}")
            c2.metric("Total Debits", f"₹{total_debit:,.2f}")
        else:
            st.info("No transactions logged yet.")

    with tab2:
        st.subheader("Add New Transaction")
        with st.form("add_transaction_form"):
            t_date = st.date_input("Date", value=datetime.today())
            t_amount = st.number_input("Amount (₹)", min_value=0.01, step=1.0)
            t_type = st.selectbox("Transaction Type", [TransactionType.CREDIT, TransactionType.DEBIT], format_func=lambda x: x.value)
            
            cat_options = {c[1]: c[0] for c in categories}
            selected_cat_name = st.selectbox("Category", list(cat_options.keys()) if cat_options else ["None"])
            t_note = st.text_area("Note / Description")
            
            submitted = st.form_submit_button("Add Transaction")
            if submitted:
                if selected_cat_name == "None" or not selected_cat_name:
                    st.error("Please create a category first.")
                else:
                    try:
                        cat_id = cat_options[selected_cat_name]
                        class TempCat:
                            def __init__(self, cid, cname):
                                self.id = cid
                                self.name = cname
                        
                        tx_obj = Transaction(
                            date=t_date,
                            amount=t_amount,
                            transaction_type=t_type,
                            category=TempCat(cat_id, selected_cat_name),
                            note=t_note
                        )
                        manager.add_transaction(tx_obj)
                        st.success("Transaction added successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to add transaction: {e}")

    with tab3:
        st.subheader("Delete Transaction")
        if not df.empty:
            tx_id_to_delete = st.selectbox("Select Transaction ID to Delete", df['id'].tolist())
            if st.button("Delete Transaction"):
                try:
                    manager.db.remove_transaction(tx_id_to_delete)
                    st.warning(f"Transaction ID {tx_id_to_delete} deleted!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error deleting transaction: {e}")
        else:
            st.info("No transactions available to delete.")
            
    db.close()

if __name__ == "__main__":
    render_transactions()