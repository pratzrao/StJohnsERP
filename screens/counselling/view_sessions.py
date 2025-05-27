import streamlit as st
import pandas as pd
from services.db_helper import fetch_all_sessions, update_session

st.title("View and Edit All Counseling Sessions")

# Column names from the JOINed query
colnames = [
    "session_id", "case_id", "session_date", "session_notes",
    "follow_up_date", "created_at", "session_type", "session_mode",
    "duration_minutes", "next_steps", "student_name"
]

# Human-readable labels
column_labels = {
    "session_id": "Session ID",
    "case_id": "Case ID",
    "session_date": "Session Date",
    "session_notes": "Session Notes",
    "follow_up_date": "Follow-Up Date",
    "created_at": "Created At",
    "session_type": "Type",
    "session_mode": "Mode",
    "duration_minutes": "Duration (min)",
    "next_steps": "Next Steps",
    "student_name": "Student Name"
}

sessions = fetch_all_sessions()
if sessions:
    df = pd.DataFrame(sessions, columns=colnames)
    
    # Reorder columns if needed
    preferred_order = [
        "session_id", "student_name", "session_date", "session_notes", "session_type",
        "session_mode", "duration_minutes", "follow_up_date", "next_steps",
        "case_id", "created_at"
    ]
    df = df[preferred_order]

    # Rename for UI
    df_display = df.rename(columns=column_labels)

    edited_df = st.data_editor(
        df_display,
        disabled=[column_labels[col] for col in ("session_id", "case_id", "created_at", "student_name")],
        key="sessions_data_editor", height=700, width=1200
    )

    rows_to_update = []
    for i, orig in df_display.iterrows():
        edited = edited_df.loc[i]
        if not orig.equals(edited):
            edited_sql = {
                key: edited[column_labels[key]]
                for key in colnames if key in column_labels and column_labels[key] in edited
            }
            session_id = df.loc[i, "session_id"]
            rows_to_update.append((edited_sql, session_id))

    if st.button("Save Changes"):
        for new_row, sid in rows_to_update:
            old_row = df[df["session_id"] == sid].iloc[0].to_dict()
            update_fields = {k: v for k, v in new_row.items() if v != old_row[k]}
            if update_fields:
                update_session(sid, **update_fields)
        st.success("Changes saved successfully.")
else:
    st.warning("No sessions found.")