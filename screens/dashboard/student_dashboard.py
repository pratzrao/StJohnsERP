import streamlit as st
import plotly.express as px
from services.db_helper import (
    fetch_student_counts, 
    fetch_stream_distribution, 
    fetch_long_absence_count
)

# Set Page Title
st.title("Student Dashboard")

# Fetch Data
student_counts = fetch_student_counts()
stream_distribution = fetch_stream_distribution()
long_absence_count = fetch_long_absence_count()

# **Big Number Metrics**
st.subheader("📌 Key Student Statistics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="🟢 Current Students", value=student_counts["Current Students"])

with col2:
    st.metric(label="🎓 Alumni", value=student_counts["Alumni"])

with col3:
    st.metric(label="🔁 Transferred Students", value=student_counts["Transferred Students"])

with col4:
    st.metric(label="⚠️ Long Absences", value=long_absence_count)

# **Stream Distribution Pie Chart**
st.subheader("📊 Student Distribution by Stream")
if stream_distribution:
    stream_labels = list(stream_distribution.keys())
    stream_values = list(stream_distribution.values())

    fig = px.pie(
        names=stream_labels,
        values=stream_values,
        title="Student Breakdown by Stream",
        hole=0.4,
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No stream data available.")