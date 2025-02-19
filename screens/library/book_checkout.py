import streamlit as st
from services.db_helper import fetch_student_ids, fetch_available_books, checkout_book

st.title("Book Checkout")

# Fetch dropdown options
students = fetch_student_ids()  # Now returns ["SJSS00001 - Siddhanth Singh", ...]
books = fetch_available_books()  # Now returns ["BK0001 - The Great Gatsby", ...]

if students and books:
    with st.form("checkout_form"):
        # Create a mapping: "SJSS00001 - Siddhanth Singh" → "SJSS00001"
        student_mapping = {option: option.split(" - ")[0] for option in students}

        # Dropdown for student selection (User sees "ID - Name", but we store only "ID")
        selected_student_display = st.selectbox("Select Student", list(student_mapping.keys()), index=0)
        student_id = student_mapping[selected_student_display]  # Extract Student ID

        # Create a mapping: "BK0001 - The Great Gatsby" → "BK0001"
        book_mapping = {option: option.split(" - ")[0] for option in books}

        # Dropdown for book selection (User sees "ID - Title", but we store only "ID")
        selected_book_display = st.selectbox("Select Book", list(book_mapping.keys()), index=0)
        book_id = book_mapping[selected_book_display]  # Extract Book ID

        # Input field for checkout date
        checkout_date = st.date_input("Checkout Date")

        # Submit button
        submit_button = st.form_submit_button("Checkout Book")

        if submit_button:
            try:
                checkout_book(book_id, student_id, checkout_date)  # Now passes only Student ID and Book ID
                st.success(f"Book {book_id} checked out successfully!")
            except Exception as e:
                st.error(f"Error: {e}")
else:
    st.error("No students or books available for checkout.")