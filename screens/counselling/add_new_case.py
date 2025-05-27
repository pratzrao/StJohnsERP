import streamlit as st
from services.db_helper import insert_new_case

st.title("Add New Counseling Case")

student_name = st.text_input("Name of Student *")
student_id = st.text_input("Student ID")
student_grade = st.text_input("Grade")
student_section = st.text_input("Section")
reason_for_case = st.text_area("Reason for Case *")
reported_by = st.text_input("Reported By")
diagnoses = st.text_area("Diagnosis")
case_notes = st.text_area("Case Notes")
date_input = st.date_input("Case Reporting Date")
date_of_case_creation = date_input.strftime("%Y-%m-%d") if date_input else ""

testing_required = st.checkbox("Student Requires External Testing")
required_test = test_administered_by = test_results = None
if testing_required:
    required_test = st.text_area("Required Tests")
    test_administered_by = st.text_input("Test Administered By")
    test_results = st.text_area("Test Results")

is_case_closed = st.checkbox("Mark case as closed")

if st.button("Add Case"):
    if not student_name or not reason_for_case:
        st.error("Student Name and Reason for Case are required.")
    else:
        insert_new_case(student_name, student_id, student_grade, student_section, reason_for_case,
                        reported_by, diagnoses, case_notes, date_of_case_creation, is_case_closed,
                        testing_required, required_test, test_administered_by, test_results)
        st.success(f"New counseling case created successfully for Student: {student_name}.")
