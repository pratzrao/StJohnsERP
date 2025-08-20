import streamlit as st
import pandas as pd
from services.db_helper import execute_query, get_connection

st.title("View Books")

# Fetch book inventory details
query = "SELECT * FROM book_inventory;"
try:
    conn = get_connection()
    result = conn.execute(query)
    books = result.fetchall()

    if books:
        # Convert result to DataFrame
        df = pd.DataFrame(books, columns=[
            "book_id", "isbn", "book_name", "book_author", 
            "book_description", "book_condition", "status"
        ])

        # Display editable data editor
        edited_df = st.data_editor(
            df,
            disabled=("book_id",),  # Disable the book_id column
            key="book_inventory_editor"
        )

        # Identify changed rows and allow saving
        if st.button("Save Changes"):
            for index, original_row in df.iterrows():
                edited_row = edited_df.loc[index]
                if not original_row.equals(edited_row):
                    # Update modified rows in the database
                    for column, value in edited_row.items():
                        if value != original_row[column]:
                            query = f"UPDATE book_inventory SET {column} = ? WHERE book_id = ?;"
                            execute_query(query, (value, edited_row["book_id"]))
                    st.success("Changes saved successfully.")
    else:
        st.error("No books available in the inventory.")
except Exception as e:
    st.error(f"Error: {e}")