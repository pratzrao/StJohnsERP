import streamlit as st
from services.db_helper import fetch_payment_history, fetch_student_ids

st.title("View Fee Payments")

# Fetch the student IDs
student_options = fetch_student_ids()

# Create a mapping of "Student ID - Name" to Student ID
student_mapping = {option: option.split(" - ")[0] for option in student_options}

# Select Student (User sees "ID - Name", but we store only "ID")
selected_display = st.selectbox("Select Student", list(student_mapping.keys()))
student_id = student_mapping[selected_display]  # Extract only Student ID

# Fetch payment history for the selected student
payment_history = fetch_payment_history(student_id)

if payment_history:
    # Show the payment history in a table or display format
    for payment in payment_history:
        st.write(f"Paid Toward: {payment['paid_toward']}, Amount Paid: {payment['amount_paid']}, Date: {payment['transaction_date']}")
else:
    st.error("No payments made by this student.")