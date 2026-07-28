import streamlit as st
import pandas as pd
from database import Database
from finance_manager import FinanceManager
from goal import Goal

st.set_page_config(page_title="Goals - MyExpenditure", page_icon="🏆", layout="wide")

def render_goals():
    st.title("🏆 Financial Goals")
    st.markdown("Establish savings goals, monitor target amounts, and track deadlines.")
    st.markdown("---")

    db = Database()
    manager = FinanceManager(db)

    try:
        goals = manager.get_all_goals()
    except Exception as e:
        st.error(f"Error loading goals: {e}")
        goals = []

    df_goals = pd.DataFrame(goals, columns=['id', 'name', 'target_amount', 'deadline']) if goals else pd.DataFrame(columns=['id', 'name', 'target_amount', 'deadline'])

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Create Goal")
        with st.form("goal_form"):
            g_name = st.text_input("Goal Name")
            g_target = st.number_input("Target Amount (₹)", min_value=1.0, step=100.0)
            g_deadline = st.date_input("Deadline Date")
            submitted = st.form_submit_button("Save Goal")

            if submitted:
                if not g_name.strip():
                    st.error("Goal name cannot be empty.")
                else:
                    try:
                        new_goal = Goal(name=g_name, target_amount=g_target, deadline=str(g_deadline))
                        manager.add_goal(new_goal)
                        st.success(f"Goal '{g_name}' saved successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error saving goal: {e}")

    with col2:
        st.subheader("Delete Goal")
        if not df_goals.empty:
            del_g = st.selectbox("Select Goal to Delete", df_goals['name'].tolist())
            if st.button("Delete Goal"):
                try:
                    manager.remove_goal(del_g)
                    st.warning(f"Goal '{del_g}' deleted!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error deleting goal: {e}")
        else:
            st.info("No active goals found.")

    st.markdown("---")
    st.subheader("Configured Goals")
    if not df_goals.empty:
        st.dataframe(df_goals, use_container_width=True)
    else:
        st.info("No financial goals configured yet.")

    db.close()

if __name__ == "__main__":
    render_goals()