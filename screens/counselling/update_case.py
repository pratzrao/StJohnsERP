import streamlit as st
from services.db_helper import update_case, fetch_all_cases

st.title("Update Counseling Case")

# Fetch case data
cases = fetch_all_cases()
case_options = {case[0]: case for case in cases}

case_id = st.selectbox("Select Case to Update", list(case_options.keys()))

if case_id:
    case_data = case_options[case_id]

    # Extract existing values
    existing_diagnosis = case_data[2] if case_data[2] else ""  # Diagnosis
    existing_case_notes = case_data[3] if case_data[3] else ""  # Case Notes
    existing_status = case_data[4]  # Case status (closed or not)

    # Input fields with pre-filled values
    diagnosis = st.text_area("Diagnosis (Optional)", value=existing_diagnosis)
    case_notes = st.text_area("Case Notes", value=existing_case_notes)
    is_case_closed = st.checkbox("Mark case as closed", value=existing_status)

    # Update button
    if st.button("Update Case"):
        update_case(case_id, "diagnosis", diagnosis)
        update_case(case_id, "case_notes", case_notes)
        update_case(case_id, "is_case_closed", is_case_closed)
        st.success(f"Case {case_id} updated successfully.")