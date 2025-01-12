import streamlit as st
import pandas as pd
from services.db_helper import fetch_all_fee_dues

st.title("View All Fees Due")

# Fetch all fees due from the database
due_fees = fetch_all_fee_dues()

if due_fees:
    # Convert the due fees to a DataFrame
    df = pd.DataFrame(due_fees)

    # Display the table with the fee dues (including student_id)
    st.dataframe(df, use_container_width=True)
else:
    st.error("No fee dues available.")