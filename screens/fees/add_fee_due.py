import streamlit as st
from services.db_helper import insert_new_fee, fetch_student_ids

st.title("Add Fee Due")

# Fetch student data for dropdown
student_options = fetch_student_ids()

# Create a mapping of "Student ID - Name" to Student ID
student_mapping = {option: option.split(" - ")[0] for option in student_options}

# Select Student (User sees "ID - Name", but we store only "ID")
selected_display = st.selectbox("Select Student", list(student_mapping.keys()))
student_id = student_mapping[selected_display]  # Extract only Student ID

#input fields for new fee
due_for = st.selectbox("Select Fees Reason", ['Tuition', 'Library Late Fees', 'Bus and Transportation'])
amount = st.number_input("Amount Due", min_value=0.0, step=0.01)
due_by = st.date_input("Due By")

# Submit button to add the fee
submit_button = st.button("Add Fee Due")

if submit_button:
    if due_for and amount > 0:
        # Insert the new fee into the database
        insert_new_fee(student_id, due_for, amount, due_by)
        st.success(f"Fee dues of {amount} added successfully for {student_id}.")
    else:
        st.error("Please fill in all fields correctly.")