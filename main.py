import streamlit as st
from services.auth_service import authenticate_user

# Streamlit App Configuration
st.set_page_config(page_title="St. John's School Management System", layout="centered")

# Authentication Functionality
def login():
    st.title("St. John's School Management System")

    # Input fields for email and password
    email = st.text_input("Email", placeholder="Enter your email")
    password = st.text_input("Password", placeholder="Enter your password", type="password")

    # Login Button
    if st.button("Login"):
        # Validate credentials
        if email and password:
            success, error = authenticate_user(email, password)
            if success:
                st.session_state["authenticated"] = True
                st.session_state["email"] = email
                st.rerun()  # Refresh the app to display authenticated content
            else:
                st.error(error)
        else:
            st.warning("Please enter both email and password.")

# Main Content for Authenticated Users
def main():
    st.header("St. John's School Management System")
    st.success(f"Welcome, {st.session_state['email']}!")
    st.write("More functionality can be added here.")

# Application Flow
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if st.session_state["authenticated"]:
    main()
else:
    login()