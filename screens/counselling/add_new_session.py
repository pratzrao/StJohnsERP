import streamlit as st
from services.db_helper import insert_new_session, fetch_cases_with_student_info

st.title("Add New Counseling Session")

# Fetch cases with student information for dropdown
case_options, case_mapping = fetch_cases_with_student_info()

# Select Case with student information (searchable dropdown)
selected_case_display = st.selectbox(
    "Select Case", 
    case_options,
    placeholder="Search for a case by student name...",
    help="Select an open case to add a session to"
)
case_id = case_mapping.get(selected_case_display, "") if selected_case_display else ""

# Input fields
session_date = st.date_input("Session Date")
session_notes = st.text_area("Session Notes", placeholder="Enter details about the session")
follow_up_date = st.date_input("Follow-up Date (Optional)", value=None)

# Submit button
if st.button("Add Session"):
    if not case_id or not session_date or not session_notes:
        st.error("Case ID, Session Date, and Notes are required.")
    else:
        insert_new_session(case_id, session_date, session_notes, follow_up_date)
        st.success(f"New counseling session added successfully for Case {case_id}.")