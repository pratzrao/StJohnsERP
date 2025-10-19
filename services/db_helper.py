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
            student_id, student_full_name, grade, section, stream, subjects, 
            enrollment_status, entered_in_sts, long_absence, sts_number,
            student_name_given_by_parent, date_of_birth, blood_group, father_name, mother_name,
            father_mobile_number, mother_mobile_number, mother_tongue, aadhar_verification_status
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
                "stream": row[4],
                "subjects": row[5],
                "enrollment_status": row[6],
                "entered_in_sts": row[7],
                "long_absence": row[8],
                "sts_number": row[9],
                "student_name_given_by_parent": row[10],
                "date_of_birth": row[11],
                "blood_group": row[12],
                "father_name": row[13],
                "mother_name": row[14],
                "father_mobile_number": row[15],
                "mother_mobile_number": row[16],
                "mother_tongue": row[17],
                "aadhar_verification_status": row[18],
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

def insert_new_case(student_id, reason_for_case, diagnosis, case_notes, is_case_closed, type_of_issue=None, is_confidential=False, student_gender=None):
    """Inserts a new counseling case into the database."""
    case_id = generate_case_id()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Handle the new fields
    type_of_issue_str = f"'{type_of_issue}'" if type_of_issue else "NULL"
    is_confidential_str = f"'{is_confidential}'" if is_confidential else "'No'"
    student_gender_str = f"'{student_gender}'" if student_gender else "NULL"
    
    query = f"""
        INSERT INTO counseling_cases (
            case_id, student_id, reason_for_case, diagnosis, case_notes, is_case_closed, type_of_issue, is_confidential, student_gender, created_at, updated_at
        ) VALUES (
            '{case_id}', '{student_id}', '{reason_for_case}', '{diagnosis}', '{case_notes}', {int(is_case_closed)}, 
            {type_of_issue_str}, {is_confidential_str}, {student_gender_str}, '{created_at}', '{created_at}'
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

def update_case(case_id, diagnosis=None, case_notes=None, is_case_closed=None, type_of_issue=None, is_confidential=None):
    """Updates an existing counseling case."""
    update_fields = []
    
    if diagnosis:
        update_fields.append(f"diagnosis = '{diagnosis}'")
    if case_notes:
        update_fields.append(f"case_notes = '{case_notes}'")
    if is_case_closed is not None:
        update_fields.append(f"is_case_closed = {int(is_case_closed)}")
    if type_of_issue:
        update_fields.append(f"type_of_issue = '{type_of_issue}'")
    if is_confidential is not None:
        confidential_value = 'Yes' if is_confidential else 'No'
        update_fields.append(f"is_confidential = '{confidential_value}'")
    
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
    """Fetches all counseling cases from the database with student details."""
    query = """
        SELECT cc.case_id, cc.student_id, sd.student_full_name, sd.grade, sd.section,
               cc.reason_for_case, cc.diagnosis, cc.case_notes, cc.is_case_closed, 
               cc.type_of_issue, cc.is_confidential, cc.student_gender, cc.created_at, cc.updated_at 
        FROM counseling_cases cc
        JOIN student_details sd ON cc.student_id = sd.student_id
        ORDER BY cc.created_at DESC;
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

def is_super_admin():
    """Check if current user is a super admin (role_id = 1)."""
    import streamlit as st
    user_roles = st.session_state.get("user_roles", [])
    return any(role["role_id"] == 1 for role in user_roles)

def is_admin():
    """Check if current user is an admin (role_id = 3)."""
    import streamlit as st
    user_roles = st.session_state.get("user_roles", [])
    return any(role["role_id"] == 3 for role in user_roles)

def can_view_confidential():
    """Check if current user can view confidential information (super admin only)."""
    return is_super_admin()

def fetch_cases_with_confidentiality_filter():
    """Fetches cases with confidentiality filtering based on user role."""
    import streamlit as st
    
    if can_view_confidential():
        # Super admin can see all cases
        return fetch_all_cases()
    else:
        # Admin and teachers cannot see confidential cases
        query = """
            SELECT cc.case_id, cc.student_id, sd.student_full_name, sd.grade, sd.section,
                   cc.reason_for_case, cc.diagnosis, cc.case_notes, cc.is_case_closed, 
                   cc.type_of_issue, cc.is_confidential, cc.created_at, cc.updated_at 
            FROM counseling_cases cc
            JOIN student_details sd ON cc.student_id = sd.student_id
            WHERE cc.is_confidential != 'Yes' OR cc.is_confidential IS NULL
            ORDER BY cc.created_at DESC;
        """
        
        try:
            conn = get_connection()
            result = conn.execute(query)
            return result.fetchall()
        except Exception as e:
            print(f"Error fetching filtered cases: {e}")
            return []

def count_hidden_confidential_cases():
    """Count how many cases are hidden due to confidentiality."""
    import streamlit as st
    
    if can_view_confidential():
        return 0  # Super admin sees all, so nothing is hidden
    
    query = """
        SELECT COUNT(*) 
        FROM counseling_cases 
        WHERE is_confidential = 'Yes';
    """
    
    try:
        conn = get_connection()
        result = conn.execute(query)
        count = result.fetchone()
        return count[0] if count else 0
    except Exception as e:
        print(f"Error counting hidden cases: {e}")
        return 0

def fetch_sessions_with_confidentiality_filter():
    """Fetches sessions with confidentiality filtering based on user role."""
    if can_view_confidential():
        # Super admin can see all sessions with student info
        query = """
            SELECT cs.session_id, cs.case_id, cc.student_id, sd.student_full_name, sd.grade, sd.section,
                   cs.session_date, cs.session_notes, cs.follow_up_date, cs.created_at
            FROM counseling_sessions cs
            JOIN counseling_cases cc ON cs.case_id = cc.case_id
            JOIN student_details sd ON cc.student_id = sd.student_id
            ORDER BY cs.session_date DESC;
        """
        try:
            conn = get_connection()
            result = conn.execute(query)
            return result.fetchall()
        except Exception as e:
            print(f"Error fetching all sessions with student info: {e}")
            return []
    else:
        # Admin and teachers cannot see sessions from confidential cases
        query = """
            SELECT cs.session_id, cs.case_id, cc.student_id, sd.student_full_name, sd.grade, sd.section,
                   cs.session_date, cs.session_notes, cs.follow_up_date, cs.created_at
            FROM counseling_sessions cs
            JOIN counseling_cases cc ON cs.case_id = cc.case_id
            JOIN student_details sd ON cc.student_id = sd.student_id
            WHERE cc.is_confidential != 'Yes' OR cc.is_confidential IS NULL
            ORDER BY cs.session_date DESC;
        """
        
        try:
            conn = get_connection()
            result = conn.execute(query)
            return result.fetchall()
        except Exception as e:
            print(f"Error fetching filtered sessions: {e}")
            return []

def fetch_sessions_for_student_with_confidentiality_filter(student_id):
    """Fetch sessions for a specific student with confidentiality filtering."""
    if can_view_confidential():
        # Super admin can see all sessions for the student with student info
        query = f"""
            SELECT cs.session_id, cs.case_id, cc.student_id, sd.student_full_name, sd.grade, sd.section,
                   cs.session_date, cs.session_notes, cs.follow_up_date, cs.created_at
            FROM counseling_sessions cs
            JOIN counseling_cases cc ON cs.case_id = cc.case_id
            JOIN student_details sd ON cc.student_id = sd.student_id
            WHERE cc.student_id = '{student_id}'
            ORDER BY cs.session_date DESC;
        """
        try:
            conn = get_connection()
            result = conn.execute(query)
            return result.fetchall()
        except Exception as e:
            print(f"Error fetching all sessions for student: {e}")
            return []
    else:
        # Admin and teachers cannot see sessions from confidential cases
        query = f"""
            SELECT cs.session_id, cs.case_id, cc.student_id, sd.student_full_name, sd.grade, sd.section,
                   cs.session_date, cs.session_notes, cs.follow_up_date, cs.created_at
            FROM counseling_sessions cs
            JOIN counseling_cases cc ON cs.case_id = cc.case_id
            JOIN student_details sd ON cc.student_id = sd.student_id
            WHERE cc.student_id = '{student_id}' AND (cc.is_confidential != 'Yes' OR cc.is_confidential IS NULL)
            ORDER BY cs.session_date DESC;
        """
        try:
            conn = get_connection()
            result = conn.execute(query)
            return result.fetchall()
        except Exception as e:
            print(f"Error fetching filtered sessions for student: {e}")
            return []

def count_hidden_confidential_sessions():
    """Count how many sessions are hidden due to confidentiality."""
    if can_view_confidential():
        return 0  # Super admin sees all, so nothing is hidden
    
    query = """
        SELECT COUNT(*) 
        FROM counseling_sessions cs
        JOIN counseling_cases cc ON cs.case_id = cc.case_id
        WHERE cc.is_confidential = 'Yes';
    """
    
    try:
        conn = get_connection()
        result = conn.execute(query)
        count = result.fetchone()
        return count[0] if count else 0
    except Exception as e:
        print(f"Error counting hidden sessions: {e}")
        return 0

def count_hidden_confidential_sessions_for_student(student_id):
    """Count how many sessions are hidden for a specific student due to confidentiality."""
    if can_view_confidential():
        return 0  # Super admin sees all, so nothing is hidden
    
    query = f"""
        SELECT COUNT(*) 
        FROM counseling_sessions cs
        JOIN counseling_cases cc ON cs.case_id = cc.case_id
        WHERE cc.student_id = '{student_id}' AND cc.is_confidential = 'Yes';
    """
    
    try:
        conn = get_connection()
        result = conn.execute(query)
        count = result.fetchone()
        return count[0] if count else 0
    except Exception as e:
        print(f"Error counting hidden sessions for student: {e}")
        return 0

def count_sessions_for_case(case_id):
    """Count how many sessions are linked to a specific case."""
    query = f"""
        SELECT COUNT(*) 
        FROM counseling_sessions 
        WHERE case_id = '{case_id}';
    """
    
    try:
        conn = get_connection()
        result = conn.execute(query)
        count = result.fetchone()
        return count[0] if count else 0
    except Exception as e:
        print(f"Error counting sessions for case: {e}")
        return 0

def delete_counseling_case(case_id):
    """Delete a counseling case and all associated sessions."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # First delete all sessions associated with this case
        sessions_query = f"DELETE FROM counseling_sessions WHERE case_id = '{case_id}'"
        cursor.execute(sessions_query)
        
        # Then delete the case
        case_query = f"DELETE FROM counseling_cases WHERE case_id = '{case_id}'"
        cursor.execute(case_query)
        
        conn.commit()
        print(f"Successfully deleted case {case_id} and all associated sessions.")
        return True
    except Exception as e:
        print(f"Error deleting case {case_id}: {e}")
        conn.rollback()
        return False

def delete_counseling_session(session_id):
    """Delete a specific counseling session."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = f"DELETE FROM counseling_sessions WHERE session_id = '{session_id}'"
        cursor.execute(query)
        conn.commit()
        print(f"Successfully deleted session {session_id}.")
        return True
    except Exception as e:
        print(f"Error deleting session {session_id}: {e}")
        conn.rollback()
        return False

# Dashboard helper functions
def get_dashboard_metrics(from_date=None, to_date=None):
    """Get dashboard metrics for a specific date range."""
    
    # Build date filter condition
    date_filter = ""
    if from_date and to_date:
        date_filter = f"AND DATE(cc.created_at) BETWEEN '{from_date}' AND '{to_date}'"
    elif from_date:
        date_filter = f"AND DATE(cc.created_at) >= '{from_date}'"
    elif to_date:
        date_filter = f"AND DATE(cc.created_at) <= '{to_date}'"
    
    try:
        conn = get_connection()
        
        # Number of sessions conducted in date range
        sessions_query = f"""
            SELECT COUNT(cs.session_id)
            FROM counseling_sessions cs
            JOIN counseling_cases cc ON cs.case_id = cc.case_id
            WHERE 1=1 {date_filter}
        """
        
        # Number of unique children counselled (who had sessions) in date range
        unique_students_query = f"""
            SELECT COUNT(DISTINCT cc.student_id)
            FROM counseling_sessions cs
            JOIN counseling_cases cc ON cs.case_id = cc.case_id
            WHERE 1=1 {date_filter}
        """
        
        # Number of new cases registered in date range
        new_cases_query = f"""
            SELECT COUNT(cc.case_id)
            FROM counseling_cases cc
            WHERE 1=1 {date_filter}
        """
        
        sessions_count = conn.execute(sessions_query).fetchone()[0]
        unique_students_count = conn.execute(unique_students_query).fetchone()[0]
        new_cases_count = conn.execute(new_cases_query).fetchone()[0]
        
        return {
            'sessions_conducted': sessions_count,
            'unique_students': unique_students_count,
            'new_cases': new_cases_count
        }
    except Exception as e:
        print(f"Error getting dashboard metrics: {e}")
        return {'sessions_conducted': 0, 'unique_students': 0, 'new_cases': 0}

def get_students_with_no_sessions(from_date=None, to_date=None):
    """Get students who have cases registered but no sessions conducted."""
    
    # Build date filter for case registration
    date_filter = ""
    if from_date and to_date:
        date_filter = f"AND DATE(cc.created_at) BETWEEN '{from_date}' AND '{to_date}'"
    elif from_date:
        date_filter = f"AND DATE(cc.created_at) >= '{from_date}'"
    elif to_date:
        date_filter = f"AND DATE(cc.created_at) <= '{to_date}'"
    
    query = f"""
        SELECT cc.case_id, cc.student_id, sd.student_full_name, sd.grade, sd.section, 
               cc.reason_for_case, cc.type_of_issue, cc.created_at
        FROM counseling_cases cc
        JOIN student_details sd ON cc.student_id = sd.student_id
        LEFT JOIN counseling_sessions cs ON cc.case_id = cs.case_id
        WHERE cs.session_id IS NULL {date_filter}
        ORDER BY cc.created_at DESC
    """
    
    try:
        conn = get_connection()
        result = conn.execute(query)
        return result.fetchall()
    except Exception as e:
        print(f"Error getting students with no sessions: {e}")
        return []

def get_issue_type_breakdown(from_date=None, to_date=None):
    """Get breakdown of cases by issue type."""
    
    date_filter = ""
    if from_date and to_date:
        date_filter = f"AND DATE(created_at) BETWEEN '{from_date}' AND '{to_date}'"
    elif from_date:
        date_filter = f"AND DATE(created_at) >= '{from_date}'"
    elif to_date:
        date_filter = f"AND DATE(created_at) <= '{to_date}'"
    
    query = f"""
        SELECT type_of_issue, COUNT(*) as count
        FROM counseling_cases
        WHERE type_of_issue IS NOT NULL {date_filter}
        GROUP BY type_of_issue
        ORDER BY count DESC
    """
    
    try:
        conn = get_connection()
        result = conn.execute(query)
        return result.fetchall()
    except Exception as e:
        print(f"Error getting issue type breakdown: {e}")
        return []

def get_gender_breakdown(from_date=None, to_date=None):
    """Get breakdown of cases by student gender."""
    
    date_filter = ""
    if from_date and to_date:
        date_filter = f"AND DATE(cc.created_at) BETWEEN '{from_date}' AND '{to_date}'"
    elif from_date:
        date_filter = f"AND DATE(cc.created_at) >= '{from_date}'"
    elif to_date:
        date_filter = f"AND DATE(cc.created_at) <= '{to_date}'"
    
    query = f"""
        SELECT cc.student_gender, COUNT(*) as count
        FROM counseling_cases cc
        WHERE cc.student_gender IS NOT NULL {date_filter}
        GROUP BY cc.student_gender
        ORDER BY count DESC
    """
    
    try:
        conn = get_connection()
        result = conn.execute(query)
        return result.fetchall()
    except Exception as e:
        print(f"Error getting gender breakdown: {e}")
        return []

def get_grade_breakdown(from_date=None, to_date=None):
    """Get breakdown of cases by student grade."""
    
    date_filter = ""
    if from_date and to_date:
        date_filter = f"AND DATE(cc.created_at) BETWEEN '{from_date}' AND '{to_date}'"
    elif from_date:
        date_filter = f"AND DATE(cc.created_at) >= '{from_date}'"
    elif to_date:
        date_filter = f"AND DATE(cc.created_at) <= '{to_date}'"
    
    query = f"""
        SELECT sd.grade, COUNT(*) as count
        FROM counseling_cases cc
        JOIN student_details sd ON cc.student_id = sd.student_id
        WHERE sd.grade IS NOT NULL {date_filter}
        GROUP BY sd.grade
        ORDER BY sd.grade
    """
    
    try:
        conn = get_connection()
        result = conn.execute(query)
        return result.fetchall()
    except Exception as e:
        print(f"Error getting grade breakdown: {e}")
        return []