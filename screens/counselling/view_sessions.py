import streamlit as st
import pandas as pd
from services.db_helper import get_connection, fetch_all_sessions

st.title("View and Edit Counseling Sessions")

# Fetch all counseling sessions
sessions = fetch_all_sessions()

if sessions:
    column_names = [
        "session_id", "case_id", "session_date", "session_notes", 
        "follow_up_date", "created_at"
    ]
    
    df = pd.DataFrame(sessions, columns=column_names)

    # Define columns that should **not** be editable
    non_editable_columns = ("session_id", "case_id", "created_at")

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
else:
    st.warning("No sessions found.")