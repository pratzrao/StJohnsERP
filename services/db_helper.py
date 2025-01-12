import libsql_experimental as libsql
import streamlit as st
from datetime import datetime

# Get database connection details from environment variables
db_url = st.secrets["DB_URL"]
auth_token = st.secrets["AUTH_TOKEN"]

if not db_url or not auth_token:
    raise Exception("Database URL or Auth Token is missing. Check your .env file.")

# Define the global connection variable
_connection = None

def get_connection():
    global _connection  # Declare _connection as global
    try:
        if _connection is None:
            _connection = libsql.connect(database=db_url, auth_token=auth_token)
            print("Established a new database connection.")
        else:
            try:
                _connection.execute("SELECT 1;")
                print("Connection is healthy.")
            except Exception as conn_error:
                if "STREAM_EXPIRED" in str(conn_error):
                    print("Connection stream expired. Reinitializing connection.")
                    _connection = libsql.connect(database=db_url, auth_token=auth_token)
                else:
                    raise conn_error
    except Exception as e:
        print(f"Error establishing connection: {e}")
        _connection = libsql.connect(database=db_url, auth_token=auth_token)
    return _connection

def fetch_user(email):
    """Fetch a user by email from the database."""
    conn = get_connection()
    query = "SELECT * FROM users WHERE email = ?;"
    try:
        result = conn.execute(query, (email,))
        user = result.fetchone()
        if user:
            return {
                "user_type_id": user[0],
                "user_type": user[1],
                "email": user[2],
                "password_hash": user[3],
                "created_at": user[4],
                "is_active": bool(user[5]),
            }
        return None
    except Exception as e:
        print(f"Error fetching user: {e}")
        return None

def fetch_student_details():
    """Fetch all student details from the database."""
    conn = get_connection()
    query = """
        SELECT 
            student_id, student_full_name, grade, section, class_teacher_id,
            stream, subjects, enrollment_status, entered_in_sts, long_absence, sts_number
        FROM student_details;
    """
    try:
        result = conn.execute(query)
        students = result.fetchall()
        return [
            {
                "student_id": row[0],
                "student_full_name": row[1],
                "grade": row[2],
                "section": row[3],
                "class_teacher_id": row[4],  # Display teacher ID for now
                "stream": row[5],
                "subjects": row[6],
                "enrollment_status": row[7],
                "entered_in_sts": row[8],
                "long_absence": row[9],
                "sts_number": row[10],
            }
            for row in students
        ]
    except Exception as e:
        print(f"Error fetching student details: {e}")
        return []
    

def execute_query(query, params=None, fetch_one=False, fetch_all=False):
    """
    Executes a database query and logs the actual query being run.
    """
    global _connection
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Format the query with parameters
        formatted_query = format_query_with_params(query, params)
        print(f"Executing query: {formatted_query}")  # Log the exact query being executed

        # Execute the formatted query
        result = cursor.execute(formatted_query)

        if fetch_one:
            return result.fetchone()
        elif fetch_all:
            return result.fetchall()

        conn.commit()
        print("Transaction committed successfully.")

    except Exception as e:
        print(f"Query failed: {e}")
        if "STREAM_EXPIRED" in str(e):
            print("Stream expired. Reinitializing connection and retrying query.")
            _connection = None
            _connection = get_connection()
            return execute_query(query, params, fetch_one, fetch_all)
        raise Exception(f"Database query failed: {e}")


def format_query_with_params(query, params):
    """
    Formats a SQL query with parameters by substituting them directly for debugging purposes.
    """
    if params:
        for param in params:
            if param is None:
                query = query.replace("?", "NULL", 1)
            elif isinstance(param, str):
                query = query.replace("?", f"'{param.replace("'", "''")}'", 1)
            else:
                query = query.replace("?", str(param), 1)
    return query

def fetch_teacher_details():
    """Fetch all teacher details from the database."""
    conn = get_connection()
    query = """
        SELECT 
            teacher_id, first_name, last_name, date_of_birth, aadhar_number, pan_number,
            gender, primary_or_high, mobile_number, address, email, marital_status, 
            emergency_contact_name, emergency_contact_relationship, emergency_contact_number, 
            job_title, grades_taught, subjects_taught, teaching_periods_per_week, date_hired, 
            full_time_or_part_time, qualification, professional_certifications, 
            years_of_experience_in_stjohns, years_of_previous_experience, additional_skills, 
            languages, bank_details, opt_in_for_pf, status
        FROM teacher_details;
    """
    try:
        result = conn.execute(query)
        teachers = result.fetchall()
        return [
            {
                "teacher_id": row[0],
                "first_name": row[1],
                "last_name": row[2],
                "date_of_birth": row[3],
                "aadhar_number": row[4],
                "pan_number": row[5],
                "gender": row[6],
                "primary_or_high": row[7],
                "mobile_number": row[8],
                "address": row[9],
                "email": row[10],
                "marital_status": row[11],
                "emergency_contact_name": row[12],
                "emergency_contact_relationship": row[13],
                "emergency_contact_number": row[14],
                "job_title": row[15],
                "grades_taught": row[16],
                "subjects_taught": row[17],
                "teaching_periods_per_week": row[18],
                "date_hired": row[19],
                "full_time_or_part_time": row[20],
                "qualification": row[21],
                "professional_certifications": row[22],
                "years_of_experience_in_stjohns": row[23],
                "years_of_previous_experience": row[24],
                "additional_skills": row[25],
                "languages": row[26],
                "bank_details": row[27],
                "opt_in_for_pf": row[28],
                "status": row[29],
            }
            for row in teachers
        ]
    except Exception as e:
        print(f"Error fetching teacher details: {e}")
        return []
    
def fetch_admin_details():
    """Fetch all admin details from the database."""
    conn = get_connection()
    query = """
        SELECT 
            admin_id, first_name, last_name, date_of_birth, aadhar_number, pan_number,
            gender, mobile_number, address, email, marital_status, emergency_contact_name, 
            emergency_contact_relationship, emergency_contact_number, job_title, date_hired, 
            full_time_or_part_time, qualification, professional_certifications, 
            years_of_experience_in_stjohns, years_of_previous_experience, additional_skills, 
            languages, bank_details, opt_in_for_pf, status
        FROM admin_details;
    """
    try:
        result = conn.execute(query)
        admins = result.fetchall()
        return [
            {
                "admin_id": row[0],
                "first_name": row[1],
                "last_name": row[2],
                "date_of_birth": row[3],
                "aadhar_number": row[4],
                "pan_number": row[5],
                "gender": row[6],
                "mobile_number": row[7],
                "address": row[8],
                "email": row[9],
                "marital_status": row[10],
                "emergency_contact_name": row[11],
                "emergency_contact_relationship": row[12],
                "emergency_contact_number": row[13],
                "job_title": row[14],
                "date_hired": row[15],
                "full_time_or_part_time": row[16],
                "qualification": row[17],
                "professional_certifications": row[18],
                "years_of_experience_in_stjohns": row[19],
                "years_of_previous_experience": row[20],
                "additional_skills": row[21],
                "languages": row[22],
                "bank_details": row[23],
                "opt_in_for_pf": row[24],
                "status": row[25],
            }
            for row in admins
        ]
    except Exception as e:
        print(f"Error fetching admin details: {e}")
        return []

def fetch_management_details():
    """Fetch all management details from the database."""
    conn = get_connection()
    query = """
        SELECT 
            management_id, first_name, last_name, date_of_birth, aadhar_number, pan_number,
            gender, mobile_number, address, email, marital_status, emergency_contact_name, 
            emergency_contact_relationship, emergency_contact_number, job_title, date_hired, 
            full_time_or_part_time, qualification, professional_certifications, 
            years_of_experience_in_stjohns, years_of_previous_experience, additional_skills, 
            languages, bank_details, opt_in_for_pf, status
        FROM management_details;
    """
    try:
        result = conn.execute(query)
        management = result.fetchall()
        return [
            {
                "management_id": row[0],
                "first_name": row[1],
                "last_name": row[2],
                "date_of_birth": row[3],
                "aadhar_number": row[4],
                "pan_number": row[5],
                "gender": row[6],
                "mobile_number": row[7],
                "address": row[8],
                "email": row[9],
                "marital_status": row[10],
                "emergency_contact_name": row[11],
                "emergency_contact_relationship": row[12],
                "emergency_contact_number": row[13],
                "job_title": row[14],
                "date_hired": row[15],
                "full_time_or_part_time": row[16],
                "qualification": row[17],
                "professional_certifications": row[18],
                "years_of_experience_in_stjohns": row[19],
                "years_of_previous_experience": row[20],
                "additional_skills": row[21],
                "languages": row[22],
                "bank_details": row[23],
                "opt_in_for_pf": row[24],
                "status": row[25],
            }
            for row in management
        ]
    except Exception as e:
        print(f"Error fetching management details: {e}")
        return []
    
def fetch_inventory_details(table_name):
    """Fetch all inventory details from the specified table."""
    conn = get_connection()
    
    # Explicitly define column mapping for each table
    if table_name == "sale_inventory":
        query = """
            SELECT 
                item_id, item_name, description, item_category, quantity, 
                cost_per_unit, selling_price, status
            FROM sale_inventory;
        """
    elif table_name == "school_inventory":
        query = """
            SELECT 
                item_id, item_name, description, item_category, quantity, 
                cost_per_unit, date_of_purchase, date_of_removal, status
            FROM school_inventory;
        """
    else:
        raise ValueError(f"Unknown table: {table_name}")

    try:
        result = conn.execute(query)
        rows = result.fetchall()
        if table_name == "sale_inventory":
            return [
                {
                    "item_id": row[0],
                    "item_name": row[1],
                    "description": row[2],
                    "item_category": row[3],
                    "quantity": row[4],
                    "cost_per_unit": row[5],
                    "selling_price": row[6],
                    "status": row[7],
                }
                for row in rows
            ]
        elif table_name == "school_inventory":
            return [
                {
                    "item_id": row[0],
                    "item_name": row[1],
                    "description": row[2],
                    "item_category": row[3],
                    "quantity": row[4],
                    "cost_per_unit": row[5],
                    "date_of_purchase": row[6],
                    "date_of_removal": row[7],
                    "status": row[8],
                }
                for row in rows
            ]
    except Exception as e:
        print(f"Error fetching inventory details from {table_name}: {e}")
        return []

def fetch_due_fees(student_id):
    query = "SELECT * FROM fees_payable WHERE student_id = ?"
    try:
        conn = get_connection()
        result = conn.execute(query, (student_id,))
        return [{"due_for": row[4], "amount": row[2], "due_by": row[3]} for row in result.fetchall()]
    except Exception as e:
        print(f"Error fetching due fees: {e}")
        return []

def fetch_all_fee_payments():
    """Fetch all fee payments for all students."""
    query = """
        SELECT transaction_id, student_id, amount_paid, transaction_date, paid_toward 
        FROM fees_payments;
    """
    try:
        conn = get_connection()
        result = conn.execute(query)
        return [
            {"transaction_id": row[0], "student_id": row[1], "amount_paid": row[2], "transaction_date": row[3], "paid_toward": row[4]}
            for row in result.fetchall()
        ]
    except Exception as e:
        print(f"Error fetching all fee payments: {e}")
        return []

def fetch_all_fee_dues():
    """Fetch all fees due for all students."""
    query = """
        SELECT payable_id, student_id, amount, due_by, due_for 
        FROM fees_payable;
    """
    try:
        conn = get_connection()
        result = conn.execute(query)
        return [
            {"payable_id": row[0], "student_id": row[1], "amount": row[2], "due_by": row[3], "due_for": row[4]}
            for row in result.fetchall()
        ]
    except Exception as e:
        print(f"Error fetching all fee dues: {e}")
        return []

def fetch_payment_history(student_id):
    query = "SELECT * FROM fees_payments WHERE student_id = ?"
    try:
        conn = get_connection()
        result = conn.execute(query, (student_id,))
        return [{"paid_toward": row[4], "amount_paid": row[2], "transaction_date": row[3]} for row in result.fetchall()]
    except Exception as e:
        print(f"Error fetching payment history: {e}")
        return []
    

def insert_new_fee(student_id, fee_name, fee_amount, due_by):
    """Insert a new fee into the fees_payable table."""
    
    # Format the due date (due_by) into the correct format
    formatted_due_by = due_by.strftime("%d/%m/%Y")  # Ensure it's in the correct format
    
    query = f"""
        INSERT INTO fees_payable (student_id, amount, due_by, due_for)
        VALUES ('{student_id}', {fee_amount}, '{formatted_due_by}', '{fee_name}');
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        print(f"Executing query (new fee): {query}")  # Debug print for raw SQL
        cursor.execute(query)
        conn.commit()
        print(f"New fee '{fee_name}' inserted successfully.")
    except Exception as e:
        print(f"Error inserting new fee: {e}")
        conn.rollback()

def insert_fee_payment(student_id, fee_name, fee_amount, amount_paid):
    """Insert a new fee payment into the fees_payments table."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Use f-strings for the SQL query
        query = f"""
            INSERT INTO fees_payments (student_id, amount_paid, transaction_date, paid_toward)
            VALUES ('{student_id}', {amount_paid}, '{str(datetime.now())}', '{fee_name}');
        """
        print(f"Executing query: {query}")  # Debug print for raw SQL
        cursor.execute(query)
        conn.commit()
        print("Fee payment inserted successfully.")
    except Exception as e:
        print(f"Error inserting fee payment: {e}")
        conn.rollback()

def delete_fee_due(student_id, fee_name):
    """Delete a fee due after payment has been made."""
    query = f"""
        DELETE FROM fees_payable
        WHERE student_id = '{student_id}' AND due_for = '{fee_name}';
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        print(f"Executing query (delete fee): {query}")  # Debug print for raw SQL
        cursor.execute(query)
        conn.commit()
        print(f"Fee '{fee_name}' cleared for student {student_id}.")
    except Exception as e:
        print(f"Error deleting fee due: {e}")
        conn.rollback()

def update_fee_due(student_id, fee_name, new_amount_due):
    """Update the amount due for an existing fee in the fees_payable table."""
    query = f"""
        UPDATE fees_payable
        SET amount = {new_amount_due}
        WHERE student_id = '{student_id}' AND due_for = '{fee_name}';
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        print(f"Executing query (update fee): {query}")  # Debug print for raw SQL
        cursor.execute(query)
        conn.commit()
        print(f"Fee '{fee_name}' updated for student {student_id} with new amount due: {new_amount_due}")
    except Exception as e:
        print(f"Error updating fee due: {e}")
        conn.rollback()
        
def fetch_checked_out_books_details():
    """
    Fetch details of all checked-out books by joining book_checkouts and book_inventory.
    """
    query = """
        SELECT 
            bc.book_id, bi.book_name, bc.student_id, bc.checkout_date, bc.return_date, bc.notes
        FROM book_checkouts bc
        INNER JOIN book_inventory bi ON bc.book_id = bi.book_id
        WHERE bi.status = 'checked_out' AND return_date is NULL;
    """
    # here changes
    try:
        conn = get_connection()
        result = conn.execute(query)
        return [
            {
                "book_id": row[0],
                "book_name": row[1],
                "student_id": row[2],
                "checkout_date": row[3],
                "return_date": row[4],
                "notes": row[5],
            }
            for row in result.fetchall()
        ]
    except Exception as e:
        print(f"Error fetching checked out book details: {e}")
        return []

def return_book(book_id, return_date, notes=None):
    """
    Return a checked-out book: Update book_checkouts and book_inventory status.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Update return_date and notes in book_checkouts using f-strings
        query_checkouts = f"""
            UPDATE book_checkouts 
            SET return_date = '{return_date}', notes = '{notes}'
            WHERE book_id = '{book_id}';
        """
        print(f"Debug: Executing query (book_checkouts): {query_checkouts}")  # Debug statement to print the raw SQL
        cursor.execute(query_checkouts)
        
        # Update book_inventory status using f-strings
        query_inventory = f"UPDATE book_inventory SET status = 'in_library' WHERE book_id = '{book_id}';"
        print(f"Debug: Executing query (book_inventory): {query_inventory}")  # Debug statement to print the raw SQL
        cursor.execute(query_inventory)
        
        conn.commit()
        print("Book return successful.")
    except Exception as e:
        print(f"Error during book return: {e}")
        conn.rollback()
        raise
     

def fetch_book_details(book_id):
    """Fetch full details of a book from the database using its book_id."""
    query = """
        SELECT 
            bi.book_id, bi.book_name, bc.student_id, bc.checkout_date, bc.return_date, bc.notes
        FROM book_checkouts bc
        INNER JOIN book_inventory bi ON bc.book_id = bi.book_id
        WHERE bc.book_id = ?;
    """
    try:
        conn = get_connection()
        result = conn.execute(query, (book_id,))
        row = result.fetchone()
        if row:
            return {
                "book_id": row[0],
                "book_name": row[1],
                "student_id": row[2],
                "checkout_date": row[3],
                "return_date": row[4],
                "notes": row[5],
            }
        return None
    except Exception as e:
        print(f"Error fetching book details: {e}")
        return None


def checkout_book(book_id, student_id, checkout_date):
    """
    Checkout a book: Insert a record into book_checkouts and update book_inventory status.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Insert into book_checkouts using f-strings for the SQL query
        query_checkouts = f"""
            INSERT INTO book_checkouts (book_id, student_id, checkout_date)
            VALUES ('{book_id}', '{student_id}', '{checkout_date}');
        """
        print(f"Debug: Executing query (book_checkouts): {query_checkouts}")  # Debug print for raw SQL
        cursor.execute(query_checkouts)

        # Update book_inventory status using f-strings for the SQL query
        query_inventory = f"UPDATE book_inventory SET status = 'checked_out' WHERE book_id = '{book_id}';"
        print(f"Debug: Executing query (book_inventory): {query_inventory}")  # Debug print for raw SQL
        cursor.execute(query_inventory)

        conn.commit()
        print("Book checkout successful.")
    except Exception as e:
        print(f"Error during book checkout: {e}")
        conn.rollback()
        raise


#fetch data for dropdowns
def fetch_student_ids():
    """Fetch all student IDs from the student_details table."""
    query = "SELECT student_id FROM student_details;"
    try:
        conn = get_connection()
        result = conn.execute(query)
        return [row[0] for row in result.fetchall()]
    except Exception as e:
        print(f"Error fetching student IDs: {e}")
        return []

def fetch_available_books():
    """Fetch book IDs from book_inventory where the status is 'in_library'."""
    query = "SELECT book_id FROM book_inventory WHERE status = 'in_library';"
    try:
        conn = get_connection()
        result = conn.execute(query)
        return [row[0] for row in result.fetchall()]
    except Exception as e:
        print(f"Error fetching available books: {e}")
        return []

def fetch_checked_out_books():
    """Fetch book IDs from book_inventory where the status is 'checked_out'."""
    query = "SELECT book_id FROM book_inventory WHERE status = 'checked_out';"
    try:
        conn = get_connection()
        result = conn.execute(query)
        return [row[0] for row in result.fetchall()]
    except Exception as e:
        print(f"Error fetching checked out books: {e}")
        return []