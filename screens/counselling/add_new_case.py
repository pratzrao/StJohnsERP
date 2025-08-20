import streamlit as st
from services.db_helper import insert_new_case, fetch_student_ids

st.title("Add New Counseling Case")

# Fetch student data for dropdown
student_options = fetch_student_ids()

# Create a mapping of "Student ID - Name" to Student ID
student_mapping = {option: option.split(" - ")[0] for option in student_options}

# Select Student (User sees "ID - Name", but we store only "ID")
selected_display = st.selectbox("Select Student", list(student_mapping.keys()))
student_id = student_mapping[selected_display]  # Extract only Student ID

# Input fields
reason_for_case = st.text_area("Reason for Case", placeholder="Enter the reason for opening this case")
diagnosis = st.text_area("Diagnosis (Optional)", placeholder="Enter diagnosis if applicable")
case_notes = st.text_area("Case Notes", placeholder="Enter any case notes or observations")

# Case status
is_case_closed = st.checkbox("Mark case as closed")

# Submit button
if st.button("Add Case"):
    if not student_id or not reason_for_case:
        st.error("Student ID and Reason for Case are required.")
    else:
        insert_new_case(student_id, reason_for_case, diagnosis, case_notes, is_case_closed)
        st.success(f"New counseling case added successfully for Student {student_id}.")