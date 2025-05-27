import streamlit as st
from datetime import datetime
from services.db_helper import fetch_all_cases, update_case

st.title("Update Counseling Case")

column_names = [
    "case_id", "student_id", "reason_for_case", "diagnosis", "case_notes",
    "is_case_closed", "created_at", "updated_at", "student_name",
    "student_grade", "student_section", "date_of_case_creation",
    "reported_by", "testing_required", "test_results", "required_test",
    "test_administered_by"
]

cases = fetch_all_cases()
case_dicts = [dict(zip(column_names, c)) for c in cases]
case_options = {f"{c['student_name']} ({c['student_id']})": c for c in case_dicts}

selected = st.selectbox("Select Case", list(case_options.keys()))
if selected:
    case_data = case_options[selected]
    case_id = case_data["case_id"]

    try:
        initial_date = datetime.strptime(case_data.get("date_of_case_creation", ""), "%Y-%m-%d").date()
    except:
        initial_date = datetime.today()

    date_input = st.date_input("Case Reporting Date", value=initial_date)
    date_of_case_creation = date_input.strftime("%Y-%m-%d")

    fields = {
        "reason_for_case": st.text_area("Reason for Case *", value=case_data.get("reason_for_case", "")),
        "diagnosis": st.text_area("Diagnosis", value=case_data.get("diagnosis", "")),
        "case_notes": st.text_area("Case Notes", value=case_data.get("case_notes", "")),
        "is_case_closed": st.checkbox("Case Closed?", value=bool(case_data.get("is_case_closed", False))),
        "student_name": st.text_input("Student Name *", value=case_data.get("student_name", "")),
        "student_grade": st.text_input("Grade", value=case_data.get("student_grade", "")),
        "student_section": st.text_input("Section", value=case_data.get("student_section", "")),
        "date_of_case_creation": date_of_case_creation,
        "reported_by": st.text_input("Reported By", value=case_data.get("reported_by", "")),
        "testing_required": st.checkbox("Testing Required", value=bool(case_data.get("testing_required", False))),
        "test_results": st.text_area("Test Results", value=case_data.get("test_results", "")),
        "required_test": st.text_input("Required Test", value=case_data.get("required_test", "")),
        "test_administered_by": st.text_input("Test Administered By", value=case_data.get("test_administered_by", ""))
    }

    if st.button("Update Case"):
        update_case(case_id, **fields)
        st.success(f"Case for {fields['student_name']} updated successfully.")
