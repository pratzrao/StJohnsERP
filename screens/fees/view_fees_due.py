import streamlit as st
from services.db_helper import fetch_due_fees, fetch_student_ids

st.title("View Fees Due")

# Fetch the student IDs
student_id = st.selectbox("Select Student ID", fetch_student_ids())

# Fetch all due fees for the selected student
due_fees = fetch_due_fees(student_id)

if due_fees:
    # Show the fees due in a table or display format
    for fee in due_fees:
        st.write(f"Fee: {fee['due_for']}, Amount: {fee['amount']}, Due By: {fee['due_by']}")
else:
    st.error("No fees due for this student.")