import streamlit as st
from services.db_helper import execute_query, get_connection

# Function to generate the next Student ID
def get_next_student_id():
    """
    Generate the next Student ID by fetching the latest one from the database.
    """
    try:
        query = "SELECT student_id FROM student_details ORDER BY student_id DESC LIMIT 1;"
        latest_id = execute_query(query, fetch_one=True)  # Fetch the latest student_id

        if latest_id and latest_id[0].startswith("SJSS"):
            # Extract numeric part, increment, and pad to 4 digits
            numeric_part = int(latest_id[0][4:])
            next_id = numeric_part + 1
            return f"SJSS{next_id:04d}"
        else:
            # If no valid student_id exists, start with SJSS0001
            return "SJSS0001"
    except Exception as e:
        st.error(f"Error generating next Student ID: {e}")
        return "ERROR"

# Fetch the next student ID
student_id = get_next_student_id()

# Function to validate form data
def validate_form(student_name, entered_in_sts, sts_number):
    error_msgs = []

    # Validate mandatory fields
    if not student_name.strip():
        error_msgs.append("Student Name is mandatory.")

    if entered_in_sts == "yes" and not sts_number.strip():
        error_msgs.append("STS Number is mandatory when Entered in STS is 'yes'.")

    return error_msgs

# Function to insert the student data into the database
def insert_student_data(student_id, student_name, grade, section, stream, subjects, entered_in_sts, sts_number):
    query = """
        INSERT INTO student_details (
            student_id, student_full_name, grade, section, class_teacher_id, stream, 
            subjects, enrollment_status, entered_in_sts, long_absence, sts_number
        ) VALUES (?, ?, ?, ?, NULL, ?, ?, ?, ?, 'no', ?);
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
        "no",  # Default for long_absence
        sts_number if entered_in_sts == "yes" else "",  # Insert empty string for sts_number if not required
    )

    execute_query(query, params)

# Form fields
st.title("Add New Student")

# Use session_state to store form values
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

student_name = st.text_input("Student Name *", value=st.session_state.student_name)
grade = st.text_input("Grade", value=st.session_state.grade)
section = st.text_input("Section", value=st.session_state.section)
stream = st.text_input("Stream", value=st.session_state.stream)
subjects = st.text_input("Subjects", value=st.session_state.subjects)

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
    validation_errors = validate_form(student_name, entered_in_sts, sts_number)
    if validation_errors:
        error_message.markdown("\n".join(validation_errors))
        return

    # Insert data into the database
    try:
        insert_student_data(student_id, student_name, grade, section, stream, subjects, entered_in_sts, sts_number)
        st.success("Student added successfully!")

    except Exception as ex:
        st.error(f"Unexpected error: {ex}")

st.text(f"Generated Student ID: {student_id}")

# Submit Button
st.button("Add Student", on_click=handle_submit)