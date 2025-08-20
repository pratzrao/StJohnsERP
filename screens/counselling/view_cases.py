import streamlit as st
import pandas as pd
from services.db_helper import get_connection, fetch_all_cases

st.title("View and Edit Counseling Cases")

# Fetch all counseling cases
cases = fetch_all_cases()

if cases:
    column_names = [
        "case_id", "student_id", "reason_for_case", "diagnosis", 
        "case_notes", "is_case_closed", "created_at", "updated_at"
    ]
    
    df = pd.DataFrame(cases, columns=column_names)

    # Define columns that should **not** be editable
    non_editable_columns = ("case_id", "student_id", "created_at", "updated_at", "is_case_closed")

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
else:
    st.warning("No cases found.")