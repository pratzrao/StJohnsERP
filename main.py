import streamlit as st

# Logout function
def logout():
    """Logs the user out and redirects to the login page."""
    st.session_state["authenticated"] = False
    st.session_state["email"] = None
    st.session_state["user_data"] = None
    st.session_state["user_roles"] = []
    st.rerun()

def has_role(role_id):
    """Check if current user has a specific role."""
    user_roles = st.session_state.get("user_roles", [])
    return any(role["role_id"] == role_id for role in user_roles)

def is_teacher():
    """Check if current user is a teacher (role_id = 2)."""
    return has_role(2)

# Initialize session state for authentication
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "user_roles" not in st.session_state:
    st.session_state["user_roles"] = []

# Define pages
pages = {
    "Login": st.Page("login.py", title="Log in", icon=":material/login:", default=True),
    "Logout": st.Page(logout, title="Log out", icon=":material/logout:"),
}

# Define sections with their pages
sections = {
    "Students": [
        st.Page("screens/students/view_students.py", title="View Students", icon=":material/groups:"),
        st.Page("screens/students/add_student.py", title="Add Student", icon=":material/person_add:"),
    ],
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
    
    # Role-based navigation
    if is_teacher():
        # Teachers only see Add New Counselling Case
        pg = st.navigation({
            "Counselling": [
                st.Page("screens/counselling/add_new_case.py", title="Add New Counselling Case", icon=":material/person_add:")
            ],
            "Account": [pages["Logout"]],
        })
    else:
        # Full navigation for admin and super_admin
        pg = st.navigation({
            "Students": sections["Students"],
            "Counselling": sections["Counselling"],
            "Account": [pages["Logout"]],
        })
else:
    # If not authenticated, show the login page
    pg = st.navigation([pages["Login"]])

# Run the selected page
pg.run()