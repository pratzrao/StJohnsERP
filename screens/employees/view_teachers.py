import streamlit as st
import pandas as pd
from services.db_helper import fetch_teacher_details, get_connection

# Fetch teacher details from the database
st.title("View/Edit Teacher Details")
teachers = fetch_teacher_details()

if teachers:
    # Convert the teacher data to a DataFrame
    df = pd.DataFrame(teachers)

    # Display the data editor table with the 'teacher_id' column disabled (non-editable)
    edited_df = st.data_editor(
        df,
        disabled=("teacher_id",),  # Disable the teacher_id column (non-editable)
        key="teacher_data_editor",
        height=500,
        width=900  # Adjust the height to suit your needs
    )

    # Identify changed rows by comparing original and edited DataFrame
    rows_to_update = []

    for index, original_row in df.iterrows():
        edited_row = edited_df.loc[index]

        # Compare original and edited rows and check for changes
        if not original_row.equals(edited_row):  
            # If there's a change, add the row to the update list
            rows_to_update.append((edited_row, original_row['teacher_id']))

    # Update function using f-strings for SQL queries
    def update_column(column_name, new_value, teacher_id):
        query = f"UPDATE teacher_details SET {column_name} = '{new_value}' WHERE teacher_id = '{teacher_id}'"
        print("Query run is - ", query)
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()  # Commit the changes to the database
        except Exception as error:
            st.error(f"Error updating {column_name}: {error}")

    # Button to save changes
    if st.button("Save Changes"):
        # Update the database with only changed rows
        for edited_row, teacher_id in rows_to_update:
            # Loop through each column in the row and update if changed
            for column_name, new_value in edited_row.items():
                if new_value != df.at[edited_row.name, column_name]:  # Check if value is changed
                    update_column(column_name, new_value, teacher_id)  # Update the column in the database
        st.success("Changes saved successfully.")
else:
    st.error("No teacher data available.")