import streamlit as st
import pandas as pd
from services.db_helper import get_connection

st.title("View Sessions Of Student")

# Step 1: Fetch list of unique students
@st.cache_data

def get_all_students():
    query = "SELECT DISTINCT student_name, student_id FROM counseling_cases ORDER BY student_name;"
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        st.error(f"Error fetching students: {e}")
        return []

# Step 2: Let user pick a student
students = get_all_students()
if not students:
    st.warning("No students found.")
    st.stop()

student_options = {f"{name} ({sid})": sid for name, sid in students}
selected_label = st.selectbox("Select a Student", list(student_options.keys()))
selected_student_id = student_options[selected_label]

# Step 3: Fetch sessions for that student
@st.cache_data

def fetch_sessions_by_student(student_id):
    query = """
        SELECT
            s.session_date, s.session_type, s.session_mode, s.duration_minutes,
            s.session_notes, s.follow_up_date, s.next_steps,
            c.case_id, c.reason_for_case
        FROM counseling_sessions s
        JOIN counseling_cases c ON s.case_id = c.case_id
        WHERE c.student_id = ?
        ORDER BY s.session_date DESC;
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (student_id,))
        return cursor.fetchall()
    except Exception as e:
        st.error(f"Error fetching sessions: {e}")
        return []

sessions = fetch_sessions_by_student(selected_student_id)

# Step 4: Show results
if sessions:
    columns = [
        "Session Date", "Type", "Mode", "Duration (min)", "Session Notes",
        "Follow-Up Date", "Next Steps", "Case ID", "Reason for Case"
    ]
    df = pd.DataFrame(sessions, columns=columns)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No sessions found for this student.")