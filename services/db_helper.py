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

# INSERT EMPLOYEES #
# Insert Management Employee
def insert_management(first_name, last_name, date_of_birth, aadhar_number, pan_number, gender,
                      mobile_number, address, email, marital_status, emergency_contact_name,
                      emergency_contact_relationship, emergency_contact_number, job_title, date_hired,
                      full_time_or_part_time, qualification, professional_certifications, 
                      years_of_experience_in_stjohns, years_of_previous_experience, additional_skills, 
                      languages, bank_details, opt_in_for_pf, status):
    """Insert new management employee into the management_details table."""
    query = f"""
        INSERT INTO management_details (
            first_name, last_name, date_of_birth, aadhar_number, pan_number, gender, mobile_number, 
            address, email, marital_status, emergency_contact_name, emergency_contact_relationship, 
            emergency_contact_number, job_title, date_hired, full_time_or_part_time, qualification, 
            professional_certifications, years_of_experience_in_stjohns, years_of_previous_experience, 
            additional_skills, languages, bank_details, opt_in_for_pf, status
        ) VALUES ('{first_name}', '{last_name}', '{date_of_birth}', '{aadhar_number}', '{pan_number}', 
                  '{gender}', '{mobile_number}', '{address}', '{email}', '{marital_status}', '{emergency_contact_name}',
                  '{emergency_contact_relationship}', '{emergency_contact_number}', '{job_title}', 
                  '{date_hired}', '{full_time_or_part_time}', '{qualification}', '{professional_certifications}', 
                  '{years_of_experience_in_stjohns}', '{years_of_previous_experience}', '{additional_skills}', 
                  '{languages}', '{bank_details}', '{opt_in_for_pf}', '{status}');
    """
    print(query)
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        print(f"Management employee {first_name} {last_name} added successfully.")
    except Exception as e:
        print(f"Error inserting management employee: {e}")
        conn.rollback()

# Insert Teacher Employee
def insert_teacher(first_name, last_name, date_of_birth, aadhar_number, pan_number, gender, mobile_number,
                   address, email, marital_status, emergency_contact_name, emergency_contact_relationship,
                   emergency_contact_number, job_title, grades_taught, subjects_taught, teaching_periods_per_week,
                   date_hired, full_time_or_part_time, qualification, professional_certifications,
                   years_of_experience_in_stjohns, years_of_previous_experience, additional_skills, languages,
                   bank_details, opt_in_for_pf, status):
    """Insert new teacher employee into the teacher_details table."""
    query = f"""
        INSERT INTO teacher_details (
            first_name, last_name, date_of_birth, aadhar_number, pan_number, gender, mobile_number, 
            address, email, marital_status, emergency_contact_name, emergency_contact_relationship, 
            emergency_contact_number, job_title, grades_taught, subjects_taught, teaching_periods_per_week, 
            date_hired, full_time_or_part_time, qualification, professional_certifications, 
            years_of_experience_in_stjohns, years_of_previous_experience, additional_skills, languages, 
            bank_details, opt_in_for_pf, status
        ) VALUES ('{first_name}', '{last_name}', '{date_of_birth}', '{aadhar_number}', '{pan_number}', 
                  '{gender}', '{mobile_number}', '{address}', '{email}', '{marital_status}', 
                  '{emergency_contact_name}', '{emergency_contact_relationship}', '{emergency_contact_number}', 
                  '{job_title}', '{grades_taught}', '{subjects_taught}', '{teaching_periods_per_week}', 
                  '{date_hired}', '{full_time_or_part_time}', '{qualification}', '{professional_certifications}', 
                  '{years_of_experience_in_stjohns}', '{years_of_previous_experience}', '{additional_skills}', 
                  '{languages}', '{bank_details}', '{opt_in_for_pf}', '{status}');
    """
    print(query)
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        print(f"Teacher employee {first_name} {last_name} added successfully.")
    except Exception as e:
        print(f"Error inserting teacher employee: {e}")
        conn.rollback()

# Insert Admin Employee
def insert_admin(first_name, last_name, date_of_birth, aadhar_number, pan_number, gender,
                 mobile_number, address, email, marital_status, emergency_contact_name,
                 emergency_contact_relationship, emergency_contact_number, job_title, date_hired,
                 qualification, status):
    """Insert new admin employee into the admin_details table."""
    query = f"""
        INSERT INTO admin_details (
            first_name, last_name, date_of_birth, aadhar_number, pan_number, gender, mobile_number, 
            address, email, marital_status, emergency_contact_name, emergency_contact_relationship, 
            emergency_contact_number, job_title, date_hired, qualification, status
        ) VALUES ('{first_name}', '{last_name}', '{date_of_birth}', '{aadhar_number}', '{pan_number}', 
                  '{gender}', '{mobile_number}', '{address}', '{email}', '{marital_status}', 
                  '{emergency_contact_name}', '{emergency_contact_relationship}', '{emergency_contact_number}', 
                  '{job_title}', '{date_hired}', '{qualification}', '{status}');
    """
    print(query)
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        print(f"Admin employee {first_name} {last_name} added successfully.")
    except Exception as e:
        print(f"Error inserting admin employee: {e}")
        conn.rollback()

# END INSERT EMPLOYEES #

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
    """Fetch all student IDs along with student names from the student_details table."""
    query = "SELECT student_id, student_full_name FROM student_details;"
    try:
        conn = get_connection()
        result = conn.execute(query)
        return [f"{row[0]} - {row[1]}" for row in result.fetchall()]  # Format: "SJSS00001 - Siddhanth Singh"
    except Exception as e:
        print(f"Error fetching student IDs: {e}")
        return []

def fetch_available_books():
    """Fetch book IDs and titles from book_inventory where the status is 'in_library'."""
    query = "SELECT book_id, book_name FROM book_inventory WHERE status = 'in_library';"
    try:
        conn = get_connection()
        result = conn.execute(query)
        return [f"{row[0]} - {row[1]}" for row in result.fetchall()]  # Format: "BK0001 - The Great Gatsby"
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
    
#SALES

def decrease_inventory(item_id, quantity_sold):
    """
    Decrease the quantity of an item in the sale_inventory table after a sale.
    """
    query = f"""
        UPDATE sale_inventory
        SET quantity = quantity - {quantity_sold}
        WHERE item_id = '{item_id}';
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        print(f"Executing query: {query}")
        cursor.execute(query)
        conn.commit()
        print(f"Inventory updated for item {item_id}.")
    except Exception as e:
        print(f"Error updating inventory: {e}")
        conn.rollback()
        raise

def fetch_latest_sale_id():
    """
    Fetch the latest base sale ID from the sale_records table,
    ignoring the hyphenated part after the base sale ID.
    """
    query = """
        SELECT sale_id
        FROM sale_records
        ORDER BY sale_id DESC
        LIMIT 1;
    """
    try:
        conn = get_connection()
        result = conn.execute(query)
        row = result.fetchone()
        if row:
            # Extract the base sale ID by removing the hyphenation
            base_sale_id = row[0].split("-")[0]  # Example: SJSSALE00001 from SJSSALE00001-2
            return base_sale_id
        return None
    except Exception as e:
        print(f"Error fetching latest sale ID: {e}")
        return None
    

def insert_sale_records(base_sale_id, sales):
    """
    Insert multiple sale records into the sale_records table.
    Automatically adds hyphenation for unique sale IDs.
    
    :param base_sale_id: The base sale ID for the transaction (e.g., "SJSSALE00001").
    :param sales: A list of dictionaries, each containing sale details.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        for idx, sale in enumerate(sales, start=1):
            # Create a hyphenated sale ID for each item
            hyphenated_sale_id = f"{base_sale_id}-{idx}"
            
            query = f"""
                INSERT INTO sale_records (
                    sale_id, item_id, student_id, sale_date, quantity, 
                    cost_per_unit, selling_price, payment_status
                ) VALUES (
                    '{hyphenated_sale_id}', '{sale['item_id']}', '{sale['student_id']}', 
                    '{sale['sale_date']}', {sale['quantity']}, {sale['cost_per_unit']}, 
                    {sale['selling_price']}, '{sale['payment_status']}'
                );
            """
            print(f"Executing query: {query}")
            cursor.execute(query)

        conn.commit()
        print(f"Sales successfully recorded under Base Sale ID {base_sale_id}.")
    except Exception as e:
        print(f"Error inserting sale records: {e}")
        conn.rollback()
        raise


def fetch_available_items():
    """Fetch item details from sale_inventory where the status is 'available'."""
    query = """
        SELECT 
            item_id, item_name, quantity, cost_per_unit, selling_price 
        FROM sale_inventory 
        WHERE status = 'available';
    """
    try:
        conn = get_connection()
        result = conn.execute(query)
        return [
            {
                "item_id": row[0],
                "item_name": row[1],
                "quantity": row[2],
                "cost_per_unit": row[3],
                "selling_price": row[4],
            }
            for row in result.fetchall()
        ]
    except Exception as e:
        print(f"Error fetching available items: {e}")
        return []
    
def fetch_sales_records():
    """Fetch all sale records from the sale_records table."""
    query = """
        SELECT 
            sale_id, item_id, student_id, sale_date, quantity, 
            cost_per_unit, selling_price, total_cost, payment_status
        FROM sale_records;
    """
    try:
        conn = get_connection()
        result = conn.execute(query)
        return [
            {
                "sale_id": row[0],
                "item_id": row[1],
                "student_id": row[2],
                "sale_date": row[3],
                "quantity": row[4],
                "cost_per_unit": row[5],
                "selling_price": row[6],
                "total_cost": row[7],
                "payment_status": row[8],
            }
            for row in result.fetchall()
        ]
    except Exception as e:
        print(f"Error fetching sales records: {e}")
        return []

#Counselling Helper Functions

# Generate Unique Case ID
def generate_case_id():
    """Generates a unique Case ID (STSCC00001, STSCC00002, etc.)."""
    query = "SELECT case_id FROM counseling_cases ORDER BY created_at DESC LIMIT 1;"
    try:
        conn = get_connection()
        result = conn.execute(query).fetchone()
        if result:
            last_id = int(result[0].replace("STSCC", "")) + 1
            return f"STSCC{last_id:05d}"
        return "STSCC00001"
    except Exception as e:
        print(f"Error generating case ID: {e}")
        return "STSCC00001"

# Generate Unique Session ID
def generate_session_id():
    """Generates a unique Session ID (STSCS00001, STSCS00002, etc.)."""
    query = "SELECT session_id FROM counseling_sessions ORDER BY created_at DESC LIMIT 1;"
    try:
        conn = get_connection()
        result = conn.execute(query).fetchone()
        if result:
            last_id = int(result[0].replace("STSCS", "")) + 1
            return f"STSCS{last_id:05d}"
        return "STSCS00001"
    except Exception as e:
        print(f"Error generating session ID: {e}")
        return "STSCS00001"

def insert_new_case(student_id, reason_for_case, diagnosis, case_notes, is_case_closed):
    """Inserts a new counseling case into the database."""
    case_id = generate_case_id()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    query = f"""
        INSERT INTO counseling_cases (
            case_id, student_id, reason_for_case, diagnosis, case_notes, is_case_closed, created_at, updated_at
        ) VALUES (
            '{case_id}', '{student_id}', '{reason_for_case}', '{diagnosis}', '{case_notes}', {int(is_case_closed)}, 
            '{created_at}', '{created_at}'
        );
    """
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        print(f"Counseling case {case_id} added successfully.")
    except Exception as e:
        print(f"Error inserting new case: {e}")
        conn.rollback()

def insert_new_session(case_id, session_date, session_notes, follow_up_date=None):
    """Inserts a new counseling session into the database."""
    session_id = generate_session_id()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    follow_up_date_str = f"'{follow_up_date}'" if follow_up_date else "NULL"
    
    query = f"""
        INSERT INTO counseling_sessions (
            session_id, case_id, session_date, session_notes, follow_up_date, created_at
        ) VALUES (
            '{session_id}', '{case_id}', '{session_date}', '{session_notes}', {follow_up_date_str}, '{created_at}'
        );
    """
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        print(f"Counseling session {session_id} added successfully.")
    except Exception as e:
        print(f"Error inserting new session: {e}")
        conn.rollback()

def update_case(case_id, diagnosis=None, case_notes=None, is_case_closed=None):
    """Updates an existing counseling case."""
    update_fields = []
    
    if diagnosis:
        update_fields.append(f"diagnosis = '{diagnosis}'")
    if case_notes:
        update_fields.append(f"case_notes = '{case_notes}'")
    if is_case_closed is not None:
        update_fields.append(f"is_case_closed = {int(is_case_closed)}")
    
    if not update_fields:
        return  # Nothing to update
    
    update_query = f"""
        UPDATE counseling_cases
        SET {', '.join(update_fields)}, updated_at = '{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        WHERE case_id = '{case_id}';
    """
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(update_query)
        conn.commit()
        print(f"Case {case_id} updated successfully.")
    except Exception as e:
        print(f"Error updating case: {e}")
        conn.rollback()

def update_session(session_id, session_notes=None, follow_up_date=None):
    """Updates an existing counseling session."""
    update_fields = []
    
    if session_notes:
        update_fields.append(f"session_notes = '{session_notes}'")
    if follow_up_date:
        update_fields.append(f"follow_up_date = '{follow_up_date}'")
    
    if not update_fields:
        return  # Nothing to update

    update_query = f"""
        UPDATE counseling_sessions
        SET {', '.join(update_fields)}
        WHERE session_id = '{session_id}';
    """
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(update_query)
        conn.commit()
        print(f"Session {session_id} updated successfully.")
    except Exception as e:
        print(f"Error updating session: {e}")
        conn.rollback()

def fetch_all_cases():
    """Fetches all counseling cases from the database."""
    query = "SELECT * FROM counseling_cases ORDER BY created_at DESC;"
    
    try:
        conn = get_connection()
        result = conn.execute(query)
        return result.fetchall()
    except Exception as e:
        print(f"Error fetching cases: {e}")
        return []

def fetch_sessions_for_case(case_id):
    """Fetches all counseling sessions linked to a case."""
    query = f"SELECT * FROM counseling_sessions WHERE case_id = '{case_id}' ORDER BY session_date DESC;"
    
    try:
        conn = get_connection()
        result = conn.execute(query)
        return result.fetchall()
    except Exception as e:
        print(f"Error fetching sessions: {e}")
        return []

def fetch_all_sessions():
    """Fetch all counseling sessions from the database, sorted by newest first."""
    conn = get_connection()
    query = "SELECT * FROM counseling_sessions ORDER BY session_date DESC;"
    try:
        result = conn.execute(query)
        sessions = result.fetchall()
        return sessions
    except Exception as e:
        print(f"Error fetching sessions: {e}")
        return []

#Dashboard helper functions

def fetch_employee_counts():
    """Fetch the total count of teachers, admin staff, and management personnel."""
    query = """
        SELECT 
            (SELECT COUNT(*) FROM teacher_details) AS teacher_count,
            (SELECT COUNT(*) FROM admin_details) AS admin_count,
            (SELECT COUNT(*) FROM management_details) AS management_count;
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        return {
            "Teachers": result[0] if result else 0,
            "Admin Staff": result[1] if result else 0,
            "Management": result[2] if result else 0,
        }
    except Exception as e:
        print(f"Error fetching employee counts: {e}")
        return {"Teachers": 0, "Admin Staff": 0, "Management": 0}

def fetch_gender_distribution():
    """Fetch the gender distribution across all employee tables."""
    query = """
        SELECT gender, COUNT(*) 
        FROM (
            SELECT gender FROM teacher_details 
            UNION ALL
            SELECT gender FROM admin_details 
            UNION ALL
            SELECT gender FROM management_details
        ) AS all_employees
        GROUP BY gender;
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return {row[0]: row[1] for row in result}
    except Exception as e:
        print(f"Error fetching gender distribution: {e}")
        return {}

def fetch_average_teacher_age():
    """Fetch the average age of teachers."""
    query = """
        SELECT AVG((strftime('%Y', 'now') - strftime('%Y', date_of_birth))) 
        FROM teacher_details 
        WHERE date_of_birth IS NOT NULL;
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        return round(result[0], 1) if result and result[0] else "N/A"
    except Exception as e:
        print(f"Error fetching average teacher age: {e}")
        return "N/A"
    
def fetch_student_counts():
    """Fetch counts for current students, alumni, and transferred students."""
    query = """
        SELECT 
            SUM(CASE WHEN enrollment_status = 'enrolled' THEN 1 ELSE 0 END) AS current_students,
            SUM(CASE WHEN enrollment_status = 'graduated' THEN 1 ELSE 0 END) AS alumni,
            SUM(CASE WHEN enrollment_status = 'transferred' THEN 1 ELSE 0 END) AS transferred_students
        FROM student_details;
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        row = cursor.fetchone()
        return {
            "Current Students": row[0] or 0,
            "Alumni": row[1] or 0,
            "Transferred Students": row[2] or 0,
        }
    except Exception as e:
        print(f"Error fetching student counts: {e}")
        return {"Current Students": 0, "Alumni": 0, "Transferred Students": 0}

def fetch_stream_distribution():
    """Fetch student distribution by stream where stream is not NULL."""
    query = """
        SELECT stream, COUNT(*) 
        FROM student_details 
        WHERE stream IS NOT NULL 
        GROUP BY stream;
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return {row[0]: row[1] for row in result}
    except Exception as e:
        print(f"Error fetching stream distribution: {e}")
        return {}

def fetch_long_absence_count():
    """Fetch count of students marked as 'long absence'."""
    query = """
        SELECT COUNT(*) 
        FROM student_details 
        WHERE long_absence = 'yes';
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        return result[0] if result else 0
    except Exception as e:
        print(f"Error fetching long absence count: {e}")
        return 0

# Financial Dashboard helper

def fetch_defaulters_list():
    """Fetch details of students who have overdue payments."""
    query = """
        SELECT s.student_id, s.student_full_name, s.grade, 
               SUM(fp.amount) AS total_due,
               COALESCE(SUM(p.amount_paid), 0) AS total_paid,
               (SUM(fp.amount) - COALESCE(SUM(p.amount_paid), 0)) AS total_pending,
               MAX(
                   substr(fp.due_by, 7, 4) || '-' || substr(fp.due_by, 4, 2) || '-' || substr(fp.due_by, 1, 2)
               ) AS due_date,
               GROUP_CONCAT(DISTINCT fp.due_for) AS reasons
        FROM student_details s
        JOIN fees_payable fp ON s.student_id = fp.student_id
        LEFT JOIN fees_payments p ON s.student_id = p.student_id
        WHERE DATE(
            substr(fp.due_by, 7, 4) || '-' || substr(fp.due_by, 4, 2) || '-' || substr(fp.due_by, 1, 2)
        ) < DATE('now', 'localtime')  -- Convert DD/MM/YYYY to YYYY-MM-DD
        GROUP BY s.student_id
        HAVING total_pending > 0;
    """
    try:
        conn = get_connection()
        result = conn.execute(query).fetchall()
        return [
            {
                "student_id": row[0],
                "student_name": row[1],
                "grade": row[2],
                "total_due": row[3],
                "total_paid": row[4],
                "total_pending": row[5],
                "due_date": row[6],
                "reasons": row[7]
            }
            for row in result
        ]
    except Exception as e:
        print(f"Error fetching defaulters list: {e}")
        return []


def fetch_defaulter_count_by_grade():
    """Fetch count of students who have overdue fees, grouped by grade."""
    query = """
        SELECT s.grade, COUNT(DISTINCT s.student_id) AS defaulter_count
        FROM student_details s
        JOIN fees_payable fp ON s.student_id = fp.student_id
        LEFT JOIN (
            SELECT student_id, SUM(amount_paid) AS total_paid 
            FROM fees_payments GROUP BY student_id
        ) AS payments ON s.student_id = payments.student_id
        WHERE DATE(
            substr(fp.due_by, 7, 4) || '-' || substr(fp.due_by, 4, 2) || '-' || substr(fp.due_by, 1, 2)
        ) < DATE('now', 'localtime') 
        AND (COALESCE(payments.total_paid, 0) < fp.amount)
        GROUP BY s.grade;
    """
    try:
        conn = get_connection()
        result = conn.execute(query).fetchall()
        return {row[0]: row[1] for row in result}  # Return dictionary {grade: count}
    except Exception as e:
        print(f"Error fetching defaulter count by grade: {e}")
        return {}

    
def fetch_total_profit():
    """Fetch total profit from sales (Total Revenue - Total Cost Price)."""
    query = """
        SELECT COALESCE(SUM(total_cost) - SUM(cost_per_unit * quantity), 0) 
        FROM sale_records;
    """
    try:
        conn = get_connection()
        result = conn.execute(query).fetchone()
        return result[0] if result and result[0] is not None else 0  # Ensure it doesn't return None
    except Exception as e:
        print(f"Error fetching total profit: {e}")
        return 0


def fetch_total_sales():
    """Fetch total revenue generated from sales."""
    query = "SELECT COALESCE(SUM(total_cost), 0) FROM sale_records;"
    try:
        conn = get_connection()
        result = conn.execute(query).fetchone()
        return result[0] if result and result[0] is not None else 0  # Ensure it doesn't return None
    except Exception as e:
        print(f"Error fetching total sales: {e}")
        return 0