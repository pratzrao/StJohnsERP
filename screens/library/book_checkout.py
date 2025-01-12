import streamlit as st
from services.db_helper import fetch_student_ids, fetch_available_books, checkout_book

st.title("Book Checkout")

# Fetch dropdown options
students = fetch_student_ids()
books = fetch_available_books()

if students and books:
    with st.form("checkout_form"):
        # Dropdown for student selection
        student_id = st.selectbox("Select Student ID", students, index=0)

        # Dropdown for book selection
        book_id = st.selectbox("Select Book ID", books, index=0)

        # Input fields for checkout and optional return date
        checkout_date = st.date_input("Checkout Date")

        # Submit button
        submit_button = st.form_submit_button("Checkout Book")

        if submit_button:
            try:
                checkout_book(book_id, student_id, checkout_date)
                st.success(f"Book {book_id} checked out successfully!")
            except Exception as e:
                st.error(f"Error: {e}")
else:
    st.error("No students or books available for checkout.")