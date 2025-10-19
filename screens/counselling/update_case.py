import streamlit as st
from services.db_helper import update_case, fetch_all_cases, fetch_all_cases_with_student_info

st.title("Update Counseling Case")

# Fetch case data with student information
case_options, case_mapping = fetch_all_cases_with_student_info()
all_cases = fetch_all_cases()
case_data_mapping = {case[0]: case for case in all_cases}

# Select case with student information (searchable dropdown)
selected_case_display = st.selectbox(
    "Select Case to Update", 
    case_options,
    placeholder="Search for a case by student name...",
    help="Select a case to update"
)
case_id = case_mapping.get(selected_case_display, "") if selected_case_display else ""

if case_id:
    case_data = case_data_mapping[case_id]

    # Extract existing values - updated to handle new fields
    existing_diagnosis = case_data[3] if case_data[3] else ""  # Diagnosis
    existing_case_notes = case_data[4] if case_data[4] else ""  # Case Notes
    existing_status = case_data[5]  # Case status (closed or not)
    existing_type_of_issue = case_data[6] if len(case_data) > 6 and case_data[6] else "Behavioral"  # Type of Issue
    existing_is_confidential = case_data[7] if len(case_data) > 7 and case_data[7] == "Yes" else False  # Confidentiality

    # Input fields with pre-filled values
    diagnosis = st.text_area("Diagnosis (Optional)", value=existing_diagnosis)
    case_notes = st.text_area("Case Notes", value=existing_case_notes)
    
    # Type of Issue dropdown
    type_of_issue = st.selectbox(
        "Type of Concern",
        ["Behavioral", "Academic", "Both"],
        index=["Behavioral", "Academic", "Both"].index(existing_type_of_issue) if existing_type_of_issue in ["Behavioral", "Academic", "Both"] else 0
    )
    
    # Confidentiality checkbox
    is_confidential = st.checkbox(
        "Mark as Confidential",
        value=existing_is_confidential,
        help="Check this box if the case contains sensitive information that should only be visible to super administrators"
    )
    
    is_case_closed = st.checkbox("Mark case as closed", value=existing_status)

    # Update button
    if st.button("Update Case"):
        update_case(case_id, diagnosis=diagnosis, case_notes=case_notes, is_case_closed=is_case_closed, type_of_issue=type_of_issue, is_confidential=is_confidential)
        st.success(f"Case {case_id} updated successfully.")