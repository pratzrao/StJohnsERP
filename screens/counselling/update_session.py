import streamlit as st
from services.db_helper import update_session, fetch_sessions_for_case, fetch_all_cases
from datetime import datetime

st.title("Update Counseling Session")

case_colnames = ["case_id", "student_id", "student_name", "student_grade", "student_section",
                 "reason_for_case", "diagnosis", "case_notes", "is_case_closed",
                 "date_of_case_creation", "reported_by", "testing_required",
                 "required_test", "test_administered_by", "test_results",
                 "created_at", "updated_at"]

cases = fetch_all_cases()
case_dicts = [dict(zip(case_colnames, c)) for c in cases]
case_options = {f"{c['student_name']} ({c['case_id']})": c for c in case_dicts}

selected_case = st.selectbox("Select Case", list(case_options.keys()))
if selected_case:
    case_id = case_options[selected_case]["case_id"]
    sessions = fetch_sessions_for_case(case_id)
    session_colnames = ["session_id", "case_id", "session_date", "session_notes", "follow_up_date",
                        "created_at", "session_type", "session_mode", "duration_minutes", "next_steps"]
    session_dicts = [dict(zip(session_colnames, s)) for s in sessions]
    session_options = {f"{s['session_date']} - {s['session_id']}": s for s in session_dicts}

    selected_session = st.selectbox("Select Session", list(session_options.keys()))
    session = session_options[selected_session]

    try:
        follow_up = datetime.strptime(session.get("follow_up_date", ""), "%Y-%m-%d").date()
    except Exception:
        follow_up = None

    session_notes = st.text_area("Session Notes *", value=session.get("session_notes", ""))
    follow_up_date = st.date_input("Follow-up Date", value=follow_up)
    session_type = st.selectbox("Type of Session", ["Initial", "Follow-up", "Crisis", "Parent Meeting"],
                                index=["Initial", "Follow-up", "Crisis", "Parent Meeting"].index(session.get("session_type", "Initial")))
    session_mode = st.selectbox("Mode of Session", ["In-person", "Phone", "Video"],
                                index=["In-person", "Phone", "Video"].index(session.get("session_mode", "In-person")))
    duration_minutes = st.number_input("Length of session in minutes", min_value=1, max_value=180,
                                       value=session.get("duration_minutes", 30), step=5)
    next_steps = st.text_area("Next Steps", value=session.get("next_steps", ""))

    if st.button("Update Session"):
        update_session(session["session_id"], session_notes=session_notes, follow_up_date=str(follow_up_date),
                       session_type=session_type, session_mode=session_mode,
                       duration_minutes=duration_minutes, next_steps=next_steps)
        st.success("Session updated successfully.")

