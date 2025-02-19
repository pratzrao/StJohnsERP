import streamlit as st

# Logout function
def logout():
    """Logs the user out and redirects to the login page."""
    st.session_state["authenticated"] = False
    st.session_state["email"] = None
    st.rerun()

# Initialize session state for authentication
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Define pages
pages = {
    "Login": st.Page("login.py", title="Log in", icon=":material/login:", default=True),
    "Logout": st.Page(logout, title="Log out", icon=":material/logout:"),
}

# Define sections with their pages
sections = {
    "Dashboards": [
        st.Page("screens/dashboard/employee_dashboard.py", title="Employee Dashboard", icon=":material/people:"),
        st.Page("screens/dashboard/student_dashboard.py", title="Student Dashboard", icon=":material/school:"),
        st.Page("screens/dashboard/financial_dashboard.py", title="Financial Dashboard", icon=":material/attach_money:"),
    ],
    "Students": [
        st.Page("screens/students/view_students.py", title="View Students", icon=":material/groups:"),
        st.Page("screens/students/add_student.py", title="Add Student", icon=":material/person_add:"),
    ],
    "Employees": [
        st.Page("screens/employees/view_teachers.py", title="View Teachers", icon=":material/person:"),
        st.Page("screens/employees/view_admins.py", title="View Admins", icon=":material/admin_panel_settings:"),
        st.Page("screens/employees/view_management.py", title="View Management", icon=":material/business_center:"),
        st.Page("screens/employees/add_employee.py", title="Add Employee", icon=":material/person_add_alt:"),
    ],
    "Inventory": [
        st.Page("screens/inventory/view_sales_inventory.py", title="Sales Inventory", icon=":material/storefront:"),
        st.Page("screens/inventory/view_school_inventory.py", title="School Inventory", icon=":material/class:"),
    ],
    "Sales": [
        st.Page("screens/sales/view_sales.py", title="View Sales", icon=":material/insights:"),
        st.Page("screens/sales/add_sale.py", title="Add Sale", icon=":material/shopping_cart:"),
    ],
    "Library": [
        st.Page("screens/library/book_checkout.py", title="Book Checkout", icon=":material/library_books:"),
        st.Page("screens/library/book_return.py", title="Book Return", icon=":material/library_books:"),
        st.Page("screens/library/view_checked_out.py", title="Checked-out Books", icon=":material/menu_book:"),
        st.Page("screens/library/view_books.py", title="View All Books", icon=":material/book:"),
    ],
    "Fees": [
        st.Page("screens/fees/view_fees_due.py", title="View Fees Due for Student", icon=":material/payments:"),
        st.Page("screens/fees/view_fees_paid.py", title="View Fees Paid for Student", icon=":material/payments:"),
        st.Page("screens/fees/add_fee_payment.py", title="Add Fee Payment", icon=":material/credit_card:"),
        st.Page("screens/fees/add_fee_due.py", title="Add Fees Due", icon=":material/credit_card:"),
        st.Page("screens/fees/view_all_fees_due.py", title="View All Fees Due", icon=":material/payments:"),
        st.Page("screens/fees/view_all_fees_paid.py", title="View All Fees Paid", icon=":material/payments:"),
    ],
    "Counselling": [
        st.Page("screens/counselling/view_cases.py", title="View Counselling Cases", icon=":material/payments:"),
        st.Page("screens/counselling/view_sessions.py", title="View Counselling Sessions", icon=":material/payments:"),
        st.Page("screens/counselling/add_new_case.py", title="Add New Counselling Case", icon=":material/credit_card:"),
        st.Page("screens/counselling/add_new_session.py", title="Add New Counselling Session", icon=":material/credit_card:"),
        st.Page("screens/counselling/update_case.py", title="Update Counselling Case", icon=":material/payments:"),
        st.Page("screens/counselling/update_session.py", title="Update Counselling Session", icon=":material/payments:"),
    ],
}

# If authenticated, show the main content
if st.session_state["authenticated"]:
    st.sidebar.write(f"Logged in as: {st.session_state['email']}")
    # Full navigation with sections
    pg = st.navigation({
        "Dashboards": sections["Dashboards"],
        "Students": sections["Students"],
        "Employees": sections["Employees"],
        "Inventory": sections["Inventory"],
        "Sales": sections["Sales"],
        "Library": sections["Library"],
        "Fees": sections["Fees"],
        "Counselling": sections["Counselling"],
        "Account": [pages["Logout"]],
    })
else:
    # If not authenticated, show the login page
    pg = st.navigation([pages["Login"]])

# Run the selected page
pg.run()