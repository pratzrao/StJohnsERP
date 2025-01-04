import streamlit as st
from streamlit import Page

# Sidebar structure
nav_structure = {
    "Dashboards": [
        ("Overview", "screens/dashboard/overview.py", "📊"),
        ("Employee Dashboard", "screens/dashboard/employee_dashboard.py", "👨‍💼"),
        ("Student Dashboard", "screens/dashboard/student_dashboard.py", "📚"),
        ("Financial Dashboard", "screens/dashboard/financial_dashboard.py", "💸"),
    ],
    "Students": [
        ("View Student Details", "screens/students/view_students.py", "👨‍🎓"),
        ("Add New Student", "screens/students/add_student.py", "➕"),
    ],
    "Employees": [
        ("View Teacher Details", "screens/employees/view_teachers.py", "🧑‍🏫"),
        ("View Admin Details", "screens/employees/view_admins.py", "🏢"),
        ("View Management Details", "screens/employees/view_management.py", "💼"),
        ("Add New Employee", "screens/employees/add_employee.py", "➕"),
    ],
    "Inventory": [
        ("View Sales Inventory", "screens/inventory/view_sales_inventory.py", "🛒"),
        ("View School Inventory", "screens/inventory/view_school_inventory.py", "🏫"),
    ],
    "Sales": [
        ("View Sales Records", "screens/sales/view_sales.py", "📈"),
        ("Add New Sale", "screens/sales/add_sale.py", "💰"),
    ],
    "Library": [
        ("Book Checkout", "screens/library/book_checkout.py", "📚"),
        ("View Checked-out Books", "screens/library/view_checked_out.py", "📖"),
        ("View All Books", "screens/library/view_books.py", "📕"),
    ],
    "Fees": [
        ("View Fee Payment Records", "screens/fees/view_fees.py", "💵"),
        ("Add Fee Payment", "screens/fees/add_fee_payment.py", "💳"),
    ],
}

def render_sidebar():
    """Render section-wise sidebar and return the list of st.Page objects."""
    st.sidebar.title("St. John's ERP")
    pages = []

    # Define pages
    for section, links in nav_structure.items():
        st.sidebar.subheader(section)
        for name, path, icon in links:
            pages.append(Page(path, title=name, icon=icon))
            st.sidebar.markdown(f"{icon} {name}")  # For visual consistency

    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state["authenticated"] = False
        st.session_state["email"] = None
        st.rerun()

    return pages