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
        cat_map = {c[0]: c[2] for c in categories}

    
        
        total_credit = sum(t[2] for t in transactions if t[4] == TransactionType.CREDIT.value)
        total_debit = sum(t[2] for t in transactions if t[4] == TransactionType.DEBIT.value)
    except Exception as e:
        st.error(f"Error fetching backend data: {e}")
        transactions, categories, cat_map = [], [], {}
        total_credit, total_debit = 0.0, 0.0

    # DB schema columns: id, uid, amount, date, transaction_type, category_id, note
    df = pd.DataFrame(transactions, columns=['id', 'uid', 'amount', 'date', 'transaction_type', 'category_id', 'note']) if transactions else pd.DataFrame(columns=['id', 'uid', 'amount', 'date', 'transaction_type', 'category_id', 'note'])

    tab1, tab2= st.tabs(["View & Filter Transactions", "Add Transaction"])

    with tab1:
         st.subheader("All Transactions")

    if not df.empty:
        df["Category Name"] = df["category_id"].map(cat_map)

        # Header
        #h1, h2, h3, h4, h5, h6, h7 = st.columns([0.8, 1, 1, 1.2, 2, 2.5, 1])
        h2, h3, h4, h5, h6, h7 = st.columns([1, 1, 1.2, 2, 2.5, 1])

        # h1.markdown("**ID**")
        h2.markdown("**Date**")
        h3.markdown("**Amount**")
        h4.markdown("**Type**")
        h5.markdown("**Category**")
        h6.markdown("**Note**")
        h7.markdown("**Action**")

        st.divider()

        # Display each transaction
        for _, row in df.iterrows():
            # c1, c2, c3, c4, c5, c6, c7 = st.columns([0.8, 1, 1, 1.2, 2, 2.5, 1])
            c2, c3, c4, c5, c6, c7 = st.columns([1, 1, 1.2, 2, 2.5, 1])

            # c1.write(row["id"])
            c2.write(str(row["date"]))
            c3.write(f"₹{row['amount']:.2f}")
            c4.write(row["transaction_type"])
            c5.write(row["Category Name"])
            c6.write(row["note"])

            if c7.button("🗑 Delete", key=f"delete_{row['id']}"):
                try:
                    manager.db.remove_transaction(row["id"])
                    st.success(f"Transaction {row['id']} deleted successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error deleting transaction: {e}")

        st.markdown("---")

        col1, col2 = st.columns(2)
        col1.metric("Total Credits", f"₹{total_credit:,.2f}")
        col2.metric("Total Debits", f"₹{total_debit:,.2f}")

    else:
        st.info("No transactions logged yet.")

    with tab2:
        st.subheader("Add New Transaction")
        with st.form("add_transaction_form"):
            t_date = st.date_input("Date", value=datetime.today())
            t_amount = st.number_input("Amount (₹)", min_value=0.01, step=1.0)
            t_type = st.selectbox("Transaction Type", [TransactionType.CREDIT, TransactionType.DEBIT], format_func=lambda x: x.value)
            
            cat_options = {c[2] : c[0] for c in categories}
            
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
                            uid=st.session_state.uid,
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

            
    db.close()

if __name__ == "__main__":
    render_transactions()