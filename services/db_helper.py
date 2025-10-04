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

def fetch_user_roles(user_type_id):
    """Fetch roles for a specific user."""
    conn = get_connection()
    query = """
        SELECT r.role_id, r.role_name, r.description 
        FROM roles r
        JOIN user_roles ur ON r.role_id = ur.role_id
        WHERE ur.user_type_id = ?;
    """
    try:
        result = conn.execute(query, (user_type_id,))
        roles = result.fetchall()
        return [{"role_id": row[0], "role_name": row[1], "description": row[2]} for row in roles]
    except Exception as e:
        print(f"Error fetching user roles: {e}")
        return []

def fetch_student_ids():
    """Fetch all student IDs with names, grades, and sections for counselling dropdowns."""
    query = "SELECT student_id, student_full_name, grade, section FROM student_details;"
    try:
        conn = get_connection()
        result = conn.execute(query)
        return [f"{row[1]} - {row[2]} {row[3]}" for row in result.fetchall()]  # Format: "Student Name - Grade Section"
    except Exception as e:
        print(f"Error fetching student IDs: {e}")
        return []

def fetch_student_ids_with_mapping():
    """Fetch student data with mapping for counselling forms."""
    query = "SELECT student_id, student_full_name, grade, section FROM student_details;"
    try:
        conn = get_connection()
        result = conn.execute(query)
        students = []
        mapping = {}
        for row in result.fetchall():
            display_text = f"{row[1]} - {row[2]} {row[3]}"  # "Student Name - Grade Section"
            students.append(display_text)
            mapping[display_text] = row[0]  # Map display text to student_id
        return students, mapping
    except Exception as e:
        print(f"Error fetching student data: {e}")
        return [], {}

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
    print(query)
    
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
    query = """
        SELECT case_id, student_id, reason_for_case, diagnosis, case_notes, is_case_closed, created_at, updated_at 
        FROM counseling_cases ORDER BY created_at DESC;
    """
    
    try:
        conn = get_connection()
        result = conn.execute(query)
        return result.fetchall()
    except Exception as e:
        print(f"Error fetching cases: {e}")
        return []

def fetch_cases_with_student_info():
    """Fetches open cases with student information for dropdown display."""
    query = """
        SELECT cc.case_id, cc.student_id, sd.student_full_name, sd.grade, sd.section, cc.reason_for_case, cc.is_case_closed
        FROM counseling_cases cc
        JOIN student_details sd ON cc.student_id = sd.student_id
        WHERE cc.is_case_closed = 0
        ORDER BY cc.created_at DESC;
    """
    
    try:
        conn = get_connection()
        result = conn.execute(query)
        cases = []
        mapping = {}
        for row in result.fetchall():
            display_text = f"{row[2]} - {row[3]} {row[4]} (Case: {row[0]})"  # "Student Name - Grade Section (Case: ID)"
            cases.append(display_text)
            mapping[display_text] = row[0]  # Map display text to case_id
        return cases, mapping
    except Exception as e:
        print(f"Error fetching cases with student info: {e}")
        return [], {}

def fetch_all_cases_with_student_info():
    """Fetches all cases (open and closed) with student information for dropdown display."""
    query = """
        SELECT cc.case_id, cc.student_id, sd.student_full_name, sd.grade, sd.section, cc.reason_for_case, cc.is_case_closed
        FROM counseling_cases cc
        JOIN student_details sd ON cc.student_id = sd.student_id
        ORDER BY cc.created_at DESC;
    """
    
    try:
        conn = get_connection()
        result = conn.execute(query)
        cases = []
        mapping = {}
        for row in result.fetchall():
            status = " (Closed)" if row[6] else " (Open)"
            display_text = f"{row[2]} - {row[3]} {row[4]} (Case: {row[0]}){status}"  # "Student Name - Grade Section (Case: ID) (Status)"
            cases.append(display_text)
            mapping[display_text] = row[0]  # Map display text to case_id
        return cases, mapping
    except Exception as e:
        print(f"Error fetching all cases with student info: {e}")
        return [], {}

def fetch_sessions_for_case(case_id):
    """Fetches all counseling sessions linked to a case."""
    query = f"""
        SELECT session_id, case_id, session_date, session_notes, follow_up_date, created_at 
        FROM counseling_sessions WHERE case_id = '{case_id}' ORDER BY session_date DESC;
    """
    
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
    query = """
        SELECT session_id, case_id, session_date, session_notes, follow_up_date, created_at 
        FROM counseling_sessions ORDER BY session_date DESC;
    """
    try:
        result = conn.execute(query)
        sessions = result.fetchall()
        return sessions
    except Exception as e:
        print(f"Error fetching sessions: {e}")
        return []

def fetch_sessions_with_student_info():
    """Fetch all counseling sessions with student information."""
    conn = get_connection()
    query = """
        SELECT cs.session_id, cs.case_id, cs.session_date, cs.session_notes, cs.follow_up_date, cs.created_at,
               cc.student_id, sd.student_full_name, sd.grade, sd.section
        FROM counseling_sessions cs
        JOIN counseling_cases cc ON cs.case_id = cc.case_id
        JOIN student_details sd ON cc.student_id = sd.student_id
        ORDER BY cs.session_date DESC;
    """
    try:
        result = conn.execute(query)
        sessions = result.fetchall()
        return sessions
    except Exception as e:
        print(f"Error fetching sessions with student info: {e}")
        return []

def fetch_sessions_for_student(student_id):
    """Fetch all counseling sessions for a specific student."""
    conn = get_connection()
    query = f"""
        SELECT cs.session_id, cs.case_id, cs.session_date, cs.session_notes, cs.follow_up_date, cs.created_at
        FROM counseling_sessions cs
        JOIN counseling_cases cc ON cs.case_id = cc.case_id
        WHERE cc.student_id = '{student_id}'
        ORDER BY cs.session_date DESC;
    """
    try:
        result = conn.execute(query)
        sessions = result.fetchall()
        return sessions
    except Exception as e:
        print(f"Error fetching sessions for student: {e}")
        return []

def check_page_access(required_role_ids):
    """Check if current user has access to a page based on required roles."""
    import streamlit as st
    
    if not st.session_state.get("authenticated", False):
        st.error("Please log in to access this page.")
        st.stop()
    
    user_roles = st.session_state.get("user_roles", [])
    user_role_ids = [role["role_id"] for role in user_roles]
    
    # Check if user has any of the required roles
    if not any(role_id in user_role_ids for role_id in required_role_ids):
        st.error("You don't have permission to access this page.")
        st.stop()
    
    return True

def check_existing_case_for_student(student_id):
    """Check if a student already has an existing counselling case."""
    conn = get_connection()
    query = """
        SELECT case_id, is_case_closed 
        FROM counseling_cases 
        WHERE student_id = ? AND is_case_closed = 0;
    """
    try:
        result = conn.execute(query, (student_id,))
        case = result.fetchone()
        return case is not None, case[0] if case else None
    except Exception as e:
        print(f"Error checking existing case: {e}")
        return False, None