import streamlit as st
import pandas as pd
from database import Database
from finance_manager import FinanceManager
from enums import TransactionType

st.set_page_config(page_title="Categories - MyExpenditure", page_icon="📁", layout="wide")

def render_categories():
    st.title("📁 Category Management")
    st.markdown("Organize your financial activities with custom and default categories.")
    st.markdown("---")

    db = Database()
    manager = FinanceManager(db)

    try:
        categories = manager.get_all_categories()
    except Exception as e:
        st.error(f"Error loading categories: {e}")
        categories = []

    df_cat = pd.DataFrame(categories, columns=['id', 'name', 'transaction_type', 'is_default']) if categories else pd.DataFrame(columns=['id', 'name', 'transaction_type', 'is_default'])

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Add New Category")
        with st.form("add_category_form"):
            cat_name = st.text_input("Category Name")
            cat_type = st.selectbox("Transaction Type", [TransactionType.CREDIT, TransactionType.DEBIT], format_func=lambda x: x.value)
            is_default = st.checkbox("Is Default Category", value=False)
            submitted = st.form_submit_button("Create Category")
            
            if submitted:
                if not cat_name.strip():
                    st.error("Category name cannot be empty.")
                else:
                    existing_names = df_cat['name'].tolist() if not df_cat.empty else []
                    if cat_name in existing_names:
                        st.error("Category already exists! Duplicate categories are prevented.")
                    else:
                        try:
                            class TempCategory:
                                def __init__(self, name, t_type, is_def):
                                    self.name = name
                                    self.transaction_type = t_type
                                    self.is_default = is_def

                            new_cat = TempCategory(cat_name, cat_type, is_default)
                            manager.add_category(new_cat)
                            st.success(f"Category '{cat_name}' added successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Failed to add category: {e}")

    with col2:
        st.subheader("Delete Category")
        if not df_cat.empty:
            del_target = st.selectbox("Select Category to Delete", df_cat['name'].tolist())
            if st.button("Delete Selected Category"):
                try:
                    manager.remove_category(del_target)
                    st.warning(f"Category '{del_target}' deleted successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error deleting category: {e}")
        else:
            st.info("No categories available for deletion.")

    st.markdown("---")
    st.subheader("Existing Categories")
    if not df_cat.empty:
        st.dataframe(df_cat, use_container_width=True)
    else:
        st.info("No categories found.")

    db.close()

if __name__ == "__main__":
    render_categories()