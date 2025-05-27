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

def insert_new_case(student_name, student_id, student_grade, student_section, reason_for_case, reported_by, diagnosis, case_notes, date_of_case_creation, is_case_closed, testing_required, required_test, test_administered_by, test_results):
    """Inserts a new counseling case into the database."""
    case_id = generate_case_id()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    query = f"""
        INSERT INTO counseling_cases (case_id, student_id, reason_for_case, diagnosis, case_notes, 
        is_case_closed, created_at, updated_at, student_name, student_grade, student_section, 
        date_of_case_creation, reported_by, testing_required, test_results,  required_test, 
        test_administered_by
        )  VALUES (
            '{case_id}','{student_id}', '{reason_for_case}','{diagnosis}','{case_notes}',
            {int(is_case_closed)},'{created_at}', '{created_at}', '{student_name}',  '{student_grade}', 
            '{student_section}', '{date_of_case_creation}', '{reported_by}', {int(testing_required)},
            '{test_results}', '{required_test}', '{test_administered_by}'
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

def insert_new_session(
    case_id, session_date, session_notes, follow_up_date=None,
    session_type=None, session_mode=None, duration_minutes=None, next_steps=None
):
    """Inserts a new counseling session into the database."""
    session_id = generate_session_id()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Format optional fields
    follow_up_date_str = f"'{follow_up_date}'" if follow_up_date else "NULL"
    session_type_str = f"'{session_type}'" if session_type else "NULL"
    session_mode_str = f"'{session_mode}'" if session_mode else "NULL"
    duration_minutes_str = str(duration_minutes) if duration_minutes is not None else "NULL"
    next_steps_str = f"'{next_steps}'" if next_steps else "NULL"

    query = f"""
        INSERT INTO counseling_sessions (
            session_id, case_id, session_date, session_notes, follow_up_date, created_at,
            session_type, session_mode, duration_minutes, next_steps
        ) VALUES (
            '{session_id}', '{case_id}', '{session_date}', '{session_notes}', {follow_up_date_str}, '{created_at}',
            {session_type_str}, {session_mode_str}, {duration_minutes_str}, {next_steps_str}
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

def update_case(case_id, **fields):
    """Updates an existing counseling case with any number of fields."""
    if not fields:
        return

    update_fields = []
    for key, value in fields.items():
        if isinstance(value, bool):
            value = int(value)
        elif isinstance(value, str):
            value = f"'{value}'"
        elif value is None:
            value = "NULL"
        update_fields.append(f"{key} = {value}")

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

def update_session(session_id, **fields):
    """Updates any field(s) for a given session_id."""
    if not fields:
        return

    update_fields = []
    for key, value in fields.items():
        if value is None:
            update_fields.append(f"{key} = NULL")
        elif isinstance(value, bool):
            update_fields.append(f"{key} = {int(value)}")
        elif isinstance(value, int):
            update_fields.append(f"{key} = {value}")
        else:
            update_fields.append(f"{key} = '{value}'")

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
    """Fetches all counseling cases from the SQLite database."""
    query = "SELECT * FROM counseling_cases ORDER BY updated_at DESC;"
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()  # returns list of tuples
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
    """Fetch all sessions with student name included."""
    conn = get_connection()
    query = """
        SELECT s.session_id, s.case_id, s.session_date, s.session_notes, 
               s.follow_up_date, s.created_at, s.session_type, s.session_mode,
               s.duration_minutes, s.next_steps,
               c.student_name
        FROM counseling_sessions s
        JOIN counseling_cases c ON s.case_id = c.case_id
        ORDER BY s.session_date DESC;
    """
    try:
        result = conn.execute(query)
        sessions = result.fetchall()
        return sessions
    except Exception as e:
        print(f"Error fetching sessions: {e}")
        return []
