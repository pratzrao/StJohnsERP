import streamlit as st
from services.db_helper import insert_new_session, fetch_all_cases

st.title("Add New Counseling Session")

# Select Case ID
case_id = st.selectbox("Select Case", fetch_all_cases())

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