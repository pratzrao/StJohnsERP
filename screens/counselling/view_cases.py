import streamlit as st
import pandas as pd
from services.db_helper import (get_connection, fetch_cases_with_confidentiality_filter, 
                               count_hidden_confidential_cases, delete_counseling_case, 
                               count_sessions_for_case)

st.title("View and Edit Counseling Cases")

# Show confidentiality message for non-super admins
hidden_count = count_hidden_confidential_cases()
if hidden_count > 0:
    st.info(f"ℹ️ {hidden_count} case(s) hidden for confidentiality")

# Fetch counseling cases based on user role
cases = fetch_cases_with_confidentiality_filter()

if cases:
    column_names = [
        "case_id", "student_id", "student_name", "grade", "section",
        "reason_for_case", "diagnosis", "case_notes", "is_case_closed", 
        "type_of_issue", "is_confidential", "student_gender", "created_at", "updated_at"
    ]
    
    df = pd.DataFrame(cases, columns=column_names)

    # Define columns that should **not** be editable
    non_editable_columns = ("case_id", "student_id", "student_name", "grade", "section", "created_at", "updated_at", "is_case_closed")

    # Editable table using Streamlit's data editor
    edited_df = st.data_editor(
        df,
        disabled=non_editable_columns,
        key="cases_data_editor",
        height=500,
        width=1000
    )

    # Identify changed rows
    rows_to_update = []
    for index, original_row in df.iterrows():
        edited_row = edited_df.loc[index]

        if not original_row.equals(edited_row):  # Check for changes
            rows_to_update.append((edited_row, original_row["case_id"]))

    # Update function for cases
    def update_case_column(column_name, new_value, case_id):
        query = f"UPDATE counseling_cases SET {column_name} = '{new_value}' WHERE case_id = '{case_id}'"
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
            for edited_row, case_id in rows_to_update:
                for column_name, new_value in edited_row.items():
                    if new_value != df.at[edited_row.name, column_name]:  
                        update_case_column(column_name, new_value, case_id)
            st.success("Changes saved successfully.")
    
    st.divider()
    
    # Delete functionality
    st.write("**Delete Case**")
    
    # Create a cleaner dropdown
    case_options = ["Select a case to delete..."]
    case_mapping = {}
    for case in cases:
        case_id = case[0]
        student_name = case[2]
        grade = case[3]
        section = case[4]
        display_text = f"{case_id} - {student_name} ({grade} {section})"
        case_options.append(display_text)
        case_mapping[display_text] = case_id
    
    selected_case = st.selectbox(
        "Choose case",
        case_options,
        label_visibility="collapsed"
    )
    
    if selected_case != "Select a case to delete...":
        case_id_to_delete = case_mapping[selected_case]
        session_count = count_sessions_for_case(case_id_to_delete)
        
        if session_count > 0:
            st.warning(f"⚠️ This will delete case {case_id_to_delete} and {session_count} associated session(s)")
        else:
            st.info(f"This will delete case {case_id_to_delete} (no sessions to delete)")
        
        if st.button("🗑️ Delete Case", type="primary"):
            if delete_counseling_case(case_id_to_delete):
                st.success(f"Case {case_id_to_delete} deleted successfully")
                st.rerun()
            else:
                st.error("Failed to delete case")

else:
    st.warning("No cases found.")