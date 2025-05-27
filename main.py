import streamlit as st

# Define sections with their pages
sections = {
    "Counselling": [
        st.Page("screens/counselling/view_cases.py", title="View All Counselling Cases", icon=":material/payments:"),
        st.Page("screens/counselling/view_sessions.py", title="View All Counselling Sessions", icon=":material/payments:"),
        st.Page("screens/counselling/view_student_sessions.py", title="View Student's Counselling Sessions", icon=":material/payments:"),
        st.Page("screens/counselling/add_new_case.py", title="Add New Counselling Case", icon=":material/credit_card:"),
        st.Page("screens/counselling/add_new_session.py", title="Add New Counselling Session", icon=":material/credit_card:"),
        st.Page("screens/counselling/update_case.py", title="Update Counselling Case", icon=":material/payments:"),
        st.Page("screens/counselling/update_session.py", title="Update Counselling Session", icon=":material/payments:"),
    ],
}

# Full navigation with sections
pg = st.navigation({
    "Counselling": sections["Counselling"],
})

# Run the selected page
pg.run()