import streamlit as st
from services.db_helper import update_session, fetch_sessions_for_case, fetch_all_cases

st.title("Update Counseling Session")

# Fetch cases
cases = fetch_all_cases()
case_options = {case[0]: case for case in cases}

case_id = st.selectbox("Select Case", list(case_options.keys()))

if case_id:
    # Fetch sessions for selected case
    sessions = fetch_sessions_for_case(case_id)
    
    if sessions:
        session_options = {s[0]: s for s in sessions}
        session_id = st.selectbox("Select Session to Update", list(session_options.keys()))

        # Fetch existing session details
        session_data = session_options[session_id]
        existing_session_notes = session_data[3] if session_data[3] else ""  # Session notes
        existing_follow_up_date = session_data[4] if session_data[4] else None  # Follow-up date

        # Input fields with pre-filled data
        session_notes = st.text_area("Session Notes", value=existing_session_notes)
        follow_up_date = st.date_input("Follow-up Date", value=existing_follow_up_date)

        if st.button("Update Session"):
            update_session(session_id, "session_notes", session_notes)
            update_session(session_id, "follow_up_date", follow_up_date)
            st.success(f"Session {session_id} updated successfully.")
    else:
        st.warning("No sessions found for this case.")