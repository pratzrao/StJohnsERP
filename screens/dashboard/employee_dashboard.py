import streamlit as st
import pandas as pd
import plotly.express as px
from services.db_helper import fetch_employee_counts, fetch_gender_distribution, fetch_average_teacher_age

# Page title
st.title("Employee Dashboard")

# Fetch data
counts = fetch_employee_counts()
gender_distribution = fetch_gender_distribution()
avg_teacher_age = fetch_average_teacher_age()

# --- Display Employee Counts as Big Numbers ---
st.subheader("Total Employees")
col1, col2, col3 = st.columns(3)
col1.metric(label="Teachers", value=counts.get("Teachers", 0))
col2.metric(label="Admin Staff", value=counts.get("Admin Staff", 0))
col3.metric(label="Management", value=counts.get("Management", 0))

# --- Gender Distribution Pie Chart ---
st.subheader("Gender Ratio of Employees")
df_gender = pd.DataFrame(list(gender_distribution.items()), columns=["Gender", "Count"])
fig_gender = px.pie(df_gender, names="Gender", values="Count", title="Gender Distribution",
                     hole=0.4)  # Creates a donut chart effect
st.plotly_chart(fig_gender, use_container_width=True)

# --- Average Age of Teachers ---
st.subheader("Average Age of Teachers")
st.metric(label="Average Teacher Age", value=f"{avg_teacher_age} years")