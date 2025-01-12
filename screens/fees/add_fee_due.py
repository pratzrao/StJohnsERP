import streamlit as st
from services.db_helper import insert_new_fee, fetch_student_ids

st.title("Add Fee Due")

# Input fields for new fee
student_id = st.selectbox("Select Student ID", fetch_student_ids())
due_for = st.text_input("Fee Description (e.g., Tuition, Library, etc.)")
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