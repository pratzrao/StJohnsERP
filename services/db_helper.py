import libsql_experimental as libsql
import streamlit as st

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
    