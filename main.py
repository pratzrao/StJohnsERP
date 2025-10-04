import streamlit as st

# Logout function
def logout():
    """Logs the user out and redirects to the login page."""
    st.session_state["authenticated"] = False
    st.session_state["email"] = None
    st.rerun()

# Initialize session state for authentication
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Define pages
pages = {
    "Login": st.Page("login.py", title="Log in", icon=":material/login:", default=True),
    "Logout": st.Page(logout, title="Log out", icon=":material/logout:"),
}

# Define sections with their pages
sections = {
    "Counselling": [
        st.Page("screens/counselling/view_cases.py", title="View Counselling Cases", icon=":material/psychology:"),
        st.Page("screens/counselling/view_sessions.py", title="View Counselling Sessions", icon=":material/event_note:"),
        st.Page("screens/counselling/add_new_case.py", title="Add New Counselling Case", icon=":material/person_add:"),
        st.Page("screens/counselling/add_new_session.py", title="Add New Counselling Session", icon=":material/add_circle:"),
        st.Page("screens/counselling/update_case.py", title="Update Counselling Case", icon=":material/edit:"),
        st.Page("screens/counselling/update_session.py", title="Update Counselling Session", icon=":material/edit_note:"),
    ],
}

# If authenticated, show the main content
if st.session_state["authenticated"]:
    st.sidebar.write(f"Logged in as: {st.session_state['email']}")
    # Full navigation with sections
    pg = st.navigation({
        "Counselling": sections["Counselling"],
        "Account": [pages["Logout"]],
    })
else:
    # If not authenticated, show the login page
    pg = st.navigation([pages["Login"]])

# Run the selected page
pg.run()