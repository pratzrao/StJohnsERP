import streamlit as st
from services.db_helper import insert_new_session, fetch_all_cases
from datetime import date

st.title("Add New Counseling Session")

column_names = ["case_id", "student_id", "student_name", "student_grade", "student_section",
                "reason_for_case", "diagnosis", "case_notes", "is_case_closed",
                "date_of_case_creation", "reported_by", "testing_required",
                "required_test", "test_administered_by", "test_results",
                "created_at", "updated_at"]

cases = fetch_all_cases()
case_dicts = [dict(zip(column_names, c)) for c in cases]
case_options = {f"{c['student_name']} ({c['case_id']})": c for c in case_dicts}

selected = st.selectbox("Select Case", list(case_options.keys()))
if selected:
    case_id = case_options[selected]["case_id"]
    session_date = st.date_input("Session Date", value=date.today())
    session_notes = st.text_area("Session Notes *")
    follow_up_date = st.date_input("Follow-up Date")
    session_type = st.selectbox("Type of Session", ["Initial", "Follow-up", "Crisis", "Parent Meeting"])
    session_mode = st.selectbox("Mode of Session", ["In-person", "Phone", "Video"])
    duration_minutes = st.number_input("Length of session in minutes", min_value=1, max_value=180, step=5)
    next_steps = st.text_area("Next Steps")

    if st.button("Add Session"):
        if not session_notes.strip():
            st.error("Session notes are required.")
        else:
            insert_new_session(case_id, session_date, session_notes, follow_up_date,
                               session_type, session_mode, duration_minutes, next_steps)
            st.success("Session added successfully.")
