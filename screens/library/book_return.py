import streamlit as st
from services.db_helper import fetch_checked_out_books, fetch_book_details, return_book

st.title("Book Return")

# Fetch the checked-out books
checked_out_books = fetch_checked_out_books()

# Check if we have any checked-out books
if checked_out_books:
    # Dropdown for selecting a checked-out book
    book_id = st.selectbox("Select Checked-out Book ID", checked_out_books)

    # Fetch full book details for the selected book
    book_details = fetch_book_details(book_id)

    if book_details:
        # Assuming 'fetch_book_details' returns a dictionary with keys like 'student_id', 'checkout_date'
        student_id = book_details["student_id"]
        checkout_date = book_details["checkout_date"]

        st.write(f"Student ID: {student_id}")
        st.write(f"Checkout Date: {checkout_date}")

        # Return date input
        return_date = st.date_input("Return Date")

        # Notes input
        notes = st.text_area("Notes (Optional)", "")

        # Return button (this isn't in a form to trigger on selection change)
        submit_button = st.button("Return Book")

        if submit_button:
            try:
                return_book(book_id, return_date, notes)
                st.success(f"Book {book_id} returned successfully!")
            except Exception as e:
                st.error(f"Error: {e}")
else:
    st.error("No checked-out books available for return.")