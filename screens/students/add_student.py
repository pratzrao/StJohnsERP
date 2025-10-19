import streamlit as st
from services.db_helper import execute_query, get_connection

# Student IDs are now pre-generated and entered manually

# Function to validate form data
def validate_form(student_id, student_name, entered_in_sts, sts_number):
    error_msgs = []

    # Validate mandatory fields
    if not student_id.strip():
        error_msgs.append("Student ID is mandatory.")
    
    if not student_name.strip():
        error_msgs.append("Student Name is mandatory.")

    if entered_in_sts == "yes" and not sts_number.strip():
        error_msgs.append("STS Number is mandatory when Entered in STS is 'yes'.")

    return error_msgs

# Function to insert the student data into the database
def insert_student_data(student_id, student_name, grade, section, stream, subjects, entered_in_sts, sts_number, 
                       student_name_given_by_parent=None, date_of_birth=None, blood_group=None, 
                       father_name=None, mother_name=None, father_mobile_number=None, 
                       mother_mobile_number=None, mother_tongue=None, aadhar_verification_status=None):
    query = """
        INSERT INTO student_details (
            student_id, student_full_name, grade, section, stream, 
            subjects, enrollment_status, entered_in_sts, long_absence, sts_number,
            student_name_given_by_parent, date_of_birth, blood_group, father_name, mother_name,
            father_mobile_number, mother_mobile_number, mother_tongue, aadhar_verification_status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'no', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    params = (
        student_id,
        student_name,
        grade,
        section,
        stream,
        subjects,
        "enrolled",
        entered_in_sts,
        sts_number if entered_in_sts == "yes" else "",
        student_name_given_by_parent,
        date_of_birth,
        blood_group,
        father_name,
        mother_name,
        father_mobile_number,
        mother_mobile_number,
        mother_tongue,
        aadhar_verification_status
    )

    execute_query(query, params)

# Form fields
st.title("Add New Student")

# Use session_state to store form values
if "student_id" not in st.session_state:
    st.session_state.student_id = ""
if "student_name" not in st.session_state:
    st.session_state.student_name = ""
if "grade" not in st.session_state:
    st.session_state.grade = ""
if "section" not in st.session_state:
    st.session_state.section = ""
if "stream" not in st.session_state:
    st.session_state.stream = ""
if "subjects" not in st.session_state:
    st.session_state.subjects = ""
if "entered_in_sts" not in st.session_state:
    st.session_state.entered_in_sts = "no"
if "sts_number" not in st.session_state:
    st.session_state.sts_number = ""

# Basic student information
student_id = st.text_input("Student ID *", value=st.session_state.student_id, help="Enter the pre-generated student ID")
student_name = st.text_input("Student Name *", value=st.session_state.student_name)
student_name_given_by_parent = st.text_input("Student Name Given by Parent")
grade = st.text_input("Grade", value=st.session_state.grade)
section = st.text_input("Section", value=st.session_state.section)
stream = st.text_input("Stream", value=st.session_state.stream)
subjects = st.text_input("Subjects", value=st.session_state.subjects)

# Personal information
date_of_birth = st.date_input("Date of Birth", value=None)
blood_group = st.selectbox("Blood Group", ["", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])

# Family information
st.write("**Family Information**")
father_name = st.text_input("Father's Name")
mother_name = st.text_input("Mother's Name")
father_mobile_number = st.text_input("Father's Mobile Number")
mother_mobile_number = st.text_input("Mother's Mobile Number")
mother_tongue = st.text_input("Mother Tongue")

# Administrative information
aadhar_verification_status = st.selectbox("Aadhar Verification Status", ["", "Verified", "Pending", "Not Provided"])

entered_in_sts = st.selectbox(
    "Entered in STS *", ["yes", "no"], index=0 if st.session_state.entered_in_sts == "no" else 1
)

# Show STS Number only if 'Entered in STS' is 'yes'
sts_number = st.text_input(
    "STS Number", 
    value=st.session_state.sts_number,
    disabled=entered_in_sts == "no",  # Disable the field if 'Entered in STS' is 'no'
)

error_message = st.empty()

# Handle form submission
def handle_submit():
    # Clear previous errors
    error_message.empty()

    # Validate form data
    validation_errors = validate_form(student_id, student_name, entered_in_sts, sts_number)
    if validation_errors:
        error_message.markdown("\n".join(validation_errors))
        return

    # Insert data into the database
    try:
        insert_student_data(
            student_id, student_name, grade, section, stream, subjects, entered_in_sts, sts_number,
            student_name_given_by_parent, date_of_birth, blood_group, 
            father_name, mother_name, father_mobile_number, 
            mother_mobile_number, mother_tongue, aadhar_verification_status
        )
        st.success("Student added successfully!")

    except Exception as ex:
        st.error(f"Unexpected error: {ex}")

# Submit Button
st.button("Add Student", on_click=handle_submit)