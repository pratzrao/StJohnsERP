import streamlit as st
import pandas as pd
from services.db_helper import (get_connection, fetch_sessions_with_confidentiality_filter, 
                               fetch_sessions_for_student_with_confidentiality_filter, 
                               fetch_student_ids_with_mapping, count_hidden_confidential_sessions,
                               count_hidden_confidential_sessions_for_student, delete_counseling_session)

st.title("View and Edit Counseling Sessions")

# Add student filter
student_options, student_mapping = fetch_student_ids_with_mapping()
student_options.insert(0, "All Students")  # Add option to show all

selected_student_display = st.selectbox(
    "Filter by Student", 
    student_options,
    placeholder="Select a student to filter...",
    help="Select a student to view only their sessions, or choose 'All Students' to view all sessions"
)

# Show confidentiality message and fetch sessions based on filter
if selected_student_display == "All Students":
    hidden_count = count_hidden_confidential_sessions()
    if hidden_count > 0:
        st.info(f"ℹ️ {hidden_count} session(s) hidden for confidentiality")
    sessions = fetch_sessions_with_confidentiality_filter()
else:
    student_id = student_mapping.get(selected_student_display, "")
    if student_id:
        hidden_count = count_hidden_confidential_sessions_for_student(student_id)
        if hidden_count > 0:
            st.info(f"ℹ️ {hidden_count} session(s) hidden for confidentiality for this student")
        sessions = fetch_sessions_for_student_with_confidentiality_filter(student_id)
    else:
        sessions = []

if sessions:
    column_names = [
        "session_id", "case_id", "student_id", "student_name", "grade", "section",
        "session_date", "session_notes", "follow_up_date", "created_at"
    ]
    
    df = pd.DataFrame(sessions, columns=column_names)

    # Define columns that should **not** be editable
    non_editable_columns = ("session_id", "case_id", "student_id", "student_name", "grade", "section", "created_at")

    # Editable table using Streamlit's data editor
    edited_df = st.data_editor(
        df,
        disabled=non_editable_columns,
        key="sessions_data_editor",
        height=500,
        width=1000
    )

    # Identify changed rows
    rows_to_update = []
    for index, original_row in df.iterrows():
        edited_row = edited_df.loc[index]

        if not original_row.equals(edited_row):  # Check for changes
            rows_to_update.append((edited_row, original_row["session_id"]))

    # Update function for sessions
    def update_session_column(column_name, new_value, session_id):
        query = f"UPDATE counseling_sessions SET {column_name} = '{new_value}' WHERE session_id = '{session_id}'"
        print("Executing query:", query)
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
        except Exception as error:
            st.error(f"Error updating {column_name}: {error}")

    # Button to save changes
    if st.button("Save Changes"):
        if rows_to_update:
            for edited_row, session_id in rows_to_update:
                for column_name, new_value in edited_row.items():
                    if new_value != df.at[edited_row.name, column_name]:  
                        update_session_column(column_name, new_value, session_id)
            st.success("Changes saved successfully.")
    
    st.divider()
    
    # Delete functionality
    st.write("**Delete Session**")
    
    # Create a cleaner dropdown
    session_options = ["Select a session to delete..."]
    session_mapping = {}
    for session in sessions:
        session_id = session[0]
        student_name = session[3]
        grade = session[4]
        section = session[5]
        session_date = session[6]
        display_text = f"{session_id} - {student_name} ({grade} {section}) - {session_date}"
        session_options.append(display_text)
        session_mapping[display_text] = session_id
    
    selected_session = st.selectbox(
        "Choose session",
        session_options,
        label_visibility="collapsed"
    )
    
    if selected_session != "Select a session to delete...":
        session_id_to_delete = session_mapping[selected_session]
        st.warning(f"⚠️ This will permanently delete session {session_id_to_delete}")
        
        if st.button("🗑️ Delete Session", type="primary"):
            if delete_counseling_session(session_id_to_delete):
                st.success(f"Session {session_id_to_delete} deleted successfully")
                st.rerun()
            else:
                st.error("Failed to delete session")

else:
    st.warning("No sessions found.")