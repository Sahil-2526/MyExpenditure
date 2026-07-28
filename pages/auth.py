import streamlit as st
from database import Database

def render_auth():
    st.title("💸 Welcome to MyExpenditure")
    st.markdown("Please log in or create an account to manage your personal finances securely.")
    
    tab_login, tab_register = st.tabs(["Login", "Sign Up"])

    db = Database()

    # --- LOGIN TAB ---
    with tab_login:
        st.subheader("Login to Your Account")
        with st.form("login_form"):
            username_input = st.text_input("Username or Email")
            password_input = st.text_input("Password", type="password")
            login_submitted = st.form_submit_button("Login")

            if login_submitted:
                if not username_input or not password_input:
                    st.error("Please fill in all fields.")
                else:
                    # Authenticate using backend login method (calls db.login)
                    uid = db.login(username_input, password_input)
                    if uid:
                        st.session_state.uid = uid
                        db.username = username_input
                        st.success("Login successful! Redirecting...")
                        st.rerun()
                    else:
                        st.error("Invalid username/email or password.")

    # --- SIGN UP / REGISTER TAB ---
    with tab_register:
        st.subheader("Create a New Account")
        with st.form("register_form"):
            reg_username = st.text_input("Choose a Username")
            reg_email = st.text_input("Email Address")
            reg_password = st.text_input("Choose a Password", type="password")
            reg_confirm_password = st.text_input("Confirm Password", type="password")
            register_submitted = st.form_submit_button("Sign Up")

            if register_submitted:
                if not reg_username or not reg_email or not reg_password:
                    st.error("All fields are required.")
                elif reg_password != reg_confirm_password:
                    st.error("Passwords do not match.")
                else:
                    # Register user via backend (calls db.register)
                    try:
                        new_uid = db.register(reg_username, reg_email, reg_password)
                        if new_uid:
                            st.success("Account created successfully! Please switch to the Login tab to sign in.")
                        else:
                            st.error("Username or email already exists. Try logging in.")
                    except Exception as e:
                        st.error(f"Registration failed: {e}")

    db.close()