import streamlit as st
import pandas as pd
from services.db_helper import fetch_checked_out_books_details

st.title("View Checked-out Books")

# Fetch details of checked-out books
checked_out_books = fetch_checked_out_books_details()

if checked_out_books:
    # Convert the data to a DataFrame
    df = pd.DataFrame(checked_out_books)

    # Display the DataFrame in a table
    st.dataframe(df, width=1000, height=600)
else:
    st.error("No books currently checked out.")