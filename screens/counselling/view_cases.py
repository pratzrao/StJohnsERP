import streamlit as st
import pandas as pd
from services.db_helper import fetch_all_cases, update_case

st.title("View and Edit All Counseling Cases")

# Actual database columns
column_names = [
    "case_id", "student_id", "reason_for_case", "diagnosis", "case_notes",
    "is_case_closed", "created_at", "updated_at", "student_name",
    "student_grade", "student_section", "date_of_case_creation",
    "reported_by", "testing_required", "test_results", "required_test",
    "test_administered_by"
]

# Human-readable column labels
column_labels = {
    "case_id": "Case ID",
    "student_id": "Student ID",
    "reason_for_case": "Reason for Case",
    "diagnosis": "Diagnosis",
    "case_notes": "Case Notes",
    "is_case_closed": "Case Closed",
    "created_at": "Created At",
    "updated_at": "Updated At",
    "student_name": "Student Name",
    "student_grade": "Grade",
    "student_section": "Section",
    "date_of_case_creation": "Date of Case Creation",
    "reported_by": "Reported By",
    "testing_required": "Testing Required",
    "test_results": "Test Results",
    "required_test": "Required Test",
    "test_administered_by": "Test Administered By"
}


# Fetch data and convert to DataFrame
cases = fetch_all_cases()
if cases:
    df = pd.DataFrame(cases, columns=column_names)

    preferred_order = [
    "case_id", "student_name", "student_grade", "student_section", "reason_for_case",
    "student_id", "diagnosis", "case_notes", "is_case_closed",
    "date_of_case_creation", "reported_by", "testing_required",
    "test_results", "required_test", "test_administered_by",
    "created_at", "updated_at"
    ]

    df_display = df.rename(columns=column_labels)
    df_display = df_display[[column_labels[col] for col in preferred_order]]

    # Editable table
    edited_df = st.data_editor(
        df_display,
        disabled=[column_labels[col] for col in ("case_id", "created_at", "updated_at")],
        key="cases_data_editor", height=600, width=1200
    )

    # Detect changed rows
    rows_to_update = []
    for i, original in df_display.iterrows():
        edited = edited_df.loc[i]
        if not original.equals(edited):
            # Convert back to SQL column names for saving
            edited_sql = {sql_key: edited[column_labels[sql_key]] for sql_key in column_names}
            rows_to_update.append((edited_sql, df.loc[i, "case_id"]))

    if st.button("Save Changes"):
        for new_row, case_id in rows_to_update:
            old_row = df[df["case_id"] == case_id].iloc[0].to_dict()
            update_fields = {k: v for k, v in new_row.items() if v != old_row[k]}
            if update_fields:
                update_case(case_id, **update_fields)
        st.success("Changes saved successfully.")
else:
    st.warning("No cases found.")