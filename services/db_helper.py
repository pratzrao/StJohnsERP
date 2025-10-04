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