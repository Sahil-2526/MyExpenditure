import streamlit as st
import pandas as pd
from database import Database
from finance_manager import FinanceManager
from budget import Budget

st.set_page_config(page_title="Budgets - MyExpenditure", page_icon="🎯", layout="wide")

def render_budgets():
    st.title("🎯 Budget Management")
    st.markdown("Set financial limits, track progress, and monitor spending alerts.")
    st.markdown("---")

    db = Database()
    manager = FinanceManager(db)

    try:
        budgets = manager.get_all_budgets()
        categories = manager.get_all_categories()
        cat_map = {c[0]: c[1] for c in categories}
    except Exception as e:
        st.error(f"Error loading budget records: {e}")
        budgets, categories, cat_map = [], [], {}

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Create or Save Budget")
        with st.form("budget_form"):
            cat_options = {c[2]: c[0] for c in categories} # name -> id
            b_cat_name = st.selectbox("Category", list(cat_options.keys()) if cat_options else ["None"])
            b_limit = st.number_input("Budget Limit Amount (₹)", min_value=1.0, step=100.0)
            b_month = st.number_input("Month (1-12)", min_value=1, max_value=12, value=7)
            b_year = st.number_input("Year", min_value=2020, max_value=2030, value=2026)
            submitted = st.form_submit_button("Save Budget")
            
            if submitted:
                if b_cat_name == "None":
                    st.error("Please pick a valid category.")
                else:
                    try:
                        cat_id = cat_options[b_cat_name]
                        class C:
                            def __init__(self, i):
                                self.id = i
                                
                        new_budget = Budget(
                            uid=st.session_state.uid,
                            category=C(cat_id),
                            limit_amount=b_limit,
                            month=b_month,
                            year=b_year
                        )
                        manager.add_budget(new_budget)
                        st.success(f"Budget for {b_cat_name} saved successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error saving budget (it might already exist for this month/year): {e}")

    with col2:
        st.subheader("Check Budget Status")
        if categories:
            check_cat = st.selectbox("Select Category to Check", list(cat_options.keys()))
            chk_month = st.number_input("Check Month", min_value=1, max_value=12, value=7, key="chk_m")
            chk_year = st.number_input("Check Year", min_value=2020, max_value=2030, value=2026, key="chk_y")
            
            if st.button("Run Budget Analysis"):
                result = manager.check_budget(check_cat, chk_month, chk_year)
                if result:
                    st.write(result)
                    if result["status"]:
                        st.success("Status: Within Budget")
                    else:
                        st.error(f"Status: Over Budget by ₹{-result['remaining']}")
                else:
                    st.warning("No budget found for this category and month/year.")
        else:
            st.info("No categories available to check budget.")

    st.markdown("---")
    st.subheader("Active Budgets List")
    if budgets:
        # DB schema: id, uid, category_id, limit_amount, month, year
        df_budgets = pd.DataFrame(budgets, columns=['id', 'uid', 'category_id', 'limit_amount', 'month', 'year'])
        df_budgets['Category Name'] = df_budgets['category_id'].map(cat_map)
        st.dataframe(df_budgets[['id', 'Category Name', 'limit_amount', 'month', 'year']], use_container_width=True)
    else:
        st.info("No active budgets configured.")

    db.close()

if __name__ == "__main__":
    render_budgets()