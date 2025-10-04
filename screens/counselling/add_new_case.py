import streamlit as st
from services.db_helper import insert_new_case, fetch_student_ids_with_mapping, check_existing_case_for_student

st.title("Add New Counseling Case")

# Check if user is a teacher (role_id = 2)
user_roles = st.session_state.get("user_roles", [])
is_teacher = any(role["role_id"] == 2 for role in user_roles)

# Fetch student data for dropdown with new format
student_options, student_mapping = fetch_student_ids_with_mapping()

# Select Student with searchable dropdown (User sees "Name - Grade Section", but we store Student ID)
selected_display = st.selectbox(
    "Select Student", 
    student_options,
    placeholder="Search for a student...",
    help="Type to search for students by name"
)
student_id = student_mapping.get(selected_display, "") if selected_display else ""

# Check for existing case if student is selected
has_existing_case = False
existing_case_id = None
if student_id:
    has_existing_case, existing_case_id = check_existing_case_for_student(student_id)

# Display warning if case already exists
if has_existing_case:
    st.warning(f"⚠️ A case already exists for this student (Case ID: {existing_case_id}). Cannot create duplicate case.")
    st.info("Please use the 'Update Counselling Case' or 'Add New Counselling Session' options instead.")

# Input fields - show different fields based on role
reason_for_case = st.text_area(
    "Reason for Case", 
    placeholder="Enter the reason for opening this case",
    disabled=has_existing_case
)

# Only show diagnosis and case notes for non-teachers
diagnosis = ""
case_notes = ""
is_case_closed = False

if not is_teacher:
    diagnosis = st.text_area(
        "Diagnosis (Optional)", 
        placeholder="Enter diagnosis if applicable",
        disabled=has_existing_case
    )
    case_notes = st.text_area(
        "Case Notes", 
        placeholder="Enter any case notes or observations",
        disabled=has_existing_case
    )
    # Case status
    is_case_closed = st.checkbox("Mark case as closed", disabled=has_existing_case)

# Submit button - disabled if case already exists
if st.button("Add Case", disabled=has_existing_case):
    if not student_id or not reason_for_case:
        st.error("Student ID and Reason for Case are required.")
    else:
        insert_new_case(student_id, reason_for_case, diagnosis, case_notes, is_case_closed)
        st.success(f"New counseling case added successfully for Student {student_id}.")