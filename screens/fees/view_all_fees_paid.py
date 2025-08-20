import streamlit as st
import pandas as pd
from services.db_helper import fetch_all_fee_payments

st.title("View All Fees Paid")

# Fetch all fee payments from the database
payment_history = fetch_all_fee_payments()

if payment_history:
    # Convert the payment history to a DataFrame
    df = pd.DataFrame(payment_history)

    # Display the table with the fee payments (including student_id)
    st.dataframe(df, use_container_width=True)
else:
    st.error("No fee payment records available.")