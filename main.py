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

def is_admin():
    """Check if current user is an admin (role_id = 3)."""
    return has_role(3)

def is_super_admin():
    """Check if current user is a super admin (role_id = 1)."""
    return has_role(1)

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
    "Dashboard": [
        st.Page("screens/dashboard/counseling_dashboard.py", title="Counseling Dashboard", icon=":material/dashboard:"),
    ],
    "Admin": [
        st.Page("screens/links.py", title="Shareable Links", icon=":material/link:"),
    ],
}

# Check if user is trying to access public survey
# This allows anyone to access the public survey without authentication
url_params = st.query_params
if "page" in url_params and url_params["page"] == "public_survey":
    # Run the public survey directly without any navigation
    exec(open("public_survey.py").read())
    st.stop()  # Stop execution to prevent showing other UI elements
elif st.session_state["authenticated"]:
    # If authenticated, show the main content
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
    elif is_admin() or is_super_admin():
        # Full navigation for admin and super_admin (both have same access to pages, confidentiality is handled within views)
        pg = st.navigation({
            "Dashboard": sections["Dashboard"],
            "Students": sections["Students"],
            "Counselling": sections["Counselling"],
            "Admin": sections["Admin"],
            "Account": [pages["Logout"]],
        })
    else:
        # Fallback for unknown roles
        pg = st.navigation([pages["Login"]])
else:
    # If not authenticated, show only the login page
    pg = st.navigation([pages["Login"]])

# Run the selected page
pg.run()