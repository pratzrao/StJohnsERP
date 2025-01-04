import streamlit as st
from services.auth_service import authenticate_user

# Display the login screen and handle authentication
st.title("Log in to St. John's ERP")

# Input fields for login credentials
email = st.text_input("Email", placeholder="Enter your email")
password = st.text_input("Password", placeholder="Enter your password", type="password")

# Check if the login button is pressed
login_button_pressed = st.button("Login")

if login_button_pressed:
    if email and password:
        # Authenticate user
        success, error = authenticate_user(email, password)
        st.write(f"Debug: Success = {success}, Error = {error}")  # Debug the result of authentication
        if success:
            # Set session state for successful login
            st.session_state["authenticated"] = True
            st.session_state["email"] = email
            st.write(f"Login successful for {email}.")  # Optional success message
            
            # Set a flag to reload and transition to main content
            st.session_state["login_success"] = True

            # Let `main.py` handle the transition by rerunning the app.
            st.rerun()
        else:
            st.error(error)  # Display error for failed authentication
    else:
        st.warning("Please enter both email and password.")