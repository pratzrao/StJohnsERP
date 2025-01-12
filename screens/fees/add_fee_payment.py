import streamlit as st
from services.db_helper import fetch_due_fees, insert_fee_payment, delete_fee_due, fetch_student_ids, update_fee_due

st.title("Add Fee Payment")

# Add New Fee checkbox at the top
add_new_fee = st.checkbox("Add New Fee")

# Fetch the student IDs
student_id = st.selectbox("Select Student ID", fetch_student_ids())

# Initialize the amount payable
amount_payable = 0.0
partial_payment = False
fee_name = None
paid_toward = None  # To store the paid_toward field

# If "Add New Fee" is selected, change the form behavior
if add_new_fee:
    # New fee input fields
    fee_name = st.text_input("New Fee Description (e.g., Bus Charges)")
    fee_amount = st.number_input("Amount for New Fee", min_value=0.0, step=0.01)
    amount_payable = fee_amount  # Amount payable for new fee
    paid_toward = fee_name  # For new fee, paid_toward is set to the fee name
else:
    # Fetch due fees for the selected student if not adding new fee
    due_fees = fetch_due_fees(student_id)

    # Dropdown to select the fee to pay
    fee_due = st.selectbox("Select Fee Due", [f"{fee['due_for']} - {fee['amount']}" for fee in due_fees])

    if fee_due:
        # Extract fee name and amount
        fee_name = fee_due.split(" - ")[0]
        amount_payable = float(fee_due.split(" - ")[1])
        paid_toward = fee_name  # Paid toward the selected fee due (the "due_for" column value)

# Show the amount payable (if any fee is due)
if fee_name and not add_new_fee:
    st.write(f"Amount Payable: {amount_payable}")
    partial_payment = st.checkbox("Partial Payment")

# Input fields for payment details
if fee_name and partial_payment:
    amount_paid = st.number_input("Amount Paid", min_value=0.0, step=0.01)
    # Ensure amount paid is less than or equal to the due amount
    if amount_paid > amount_payable:
        st.error("Amount paid cannot be greater than the amount due.")
else:
    amount_paid = amount_payable  # Full payment selected, no need to enter manually

transaction_date = st.date_input("Transaction Date")

# Submit button to make the payment
submit_button = st.button("Submit Payment")

if submit_button:
    if amount_paid > 0:
        if add_new_fee:  # New fee payment
            # Insert the fee payment into fees_payments
            insert_fee_payment(student_id, fee_name, amount_paid, amount_paid)
            st.success(f"New fee '{fee_name}' of {amount_paid} added and payment made.")
        
        elif fee_name:  # Existing fee payment
            if partial_payment:  # Partial payment
                if amount_paid <= amount_payable:
                    # Update the fee record with partial payment (update fees_payable)
                    new_amount_due = amount_payable - amount_paid
                    update_fee_due(student_id, fee_name, new_amount_due)
                    insert_fee_payment(student_id, fee_name, amount_paid, amount_paid)
                    st.success(f"Partial payment of {amount_paid} for {fee_name} made. Amount remaining: {new_amount_due}")
                else:
                    st.error("Amount paid cannot exceed the amount due.")
            else:  # Full payment
                # Insert full payment and delete the fee record from fees_payable
                insert_fee_payment(student_id, fee_name, amount_payable, amount_paid)
                delete_fee_due(student_id, fee_name)
                st.success(f"Full payment of {amount_paid} for {fee_name} made. Fee cleared.")
    else:
        st.error("Amount Paid must be greater than 0.")