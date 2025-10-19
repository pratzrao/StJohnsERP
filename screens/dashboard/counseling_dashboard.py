import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
from services.db_helper import (
    get_dashboard_metrics,
    get_students_with_no_sessions,
    get_issue_type_breakdown,
    get_gender_breakdown,
    get_grade_breakdown,
)

st.title("Counseling Dashboard")

# Time filter section in a collapsible expander
with st.expander("⏰ Time Filter", expanded=True):
    # Filter type selection with radio buttons
    filter_type = st.radio(
        "Choose filter type:",
        ["Show All Data", "Custom Date Range", "Quick Period"],
        horizontal=True,
        help="Select how you want to filter the dashboard data"
    )
    
    # Initialize variables
    from_date_str = None
    to_date_str = None
    filter_info = "Showing all data"
    
    if filter_type == "Custom Date Range":
        st.write("**📅 Select Custom Date Range**")
        col1, col2 = st.columns(2)
        
        with col1:
            from_date = st.date_input(
                "From Date",
                value=date.today() - timedelta(days=30),
                help="Filter data from this date onwards"
            )
        
        with col2:
            to_date = st.date_input(
                "To Date", 
                value=date.today(), 
                help="Filter data up to this date"
            )
        
        from_date_str = from_date.strftime("%Y-%m-%d") if from_date else None
        to_date_str = to_date.strftime("%Y-%m-%d") if to_date else None
        filter_info = f"Showing data from {from_date} to {to_date}"
        
    elif filter_type == "Quick Period":
        st.write("**⚡ Select Quick Period**")
        selected_period = st.selectbox(
            "Choose time period:",
            ["Past Week", "Past Month", "Past Quarter", "Past Year"],
            help="Quick filter for common time periods"
        )
        
        # Calculate date range for selected period
        today = date.today()
        if selected_period == "Past Week":
            from_date_calc = today - timedelta(days=7)
        elif selected_period == "Past Month":
            from_date_calc = today - timedelta(days=30)
        elif selected_period == "Past Quarter":
            from_date_calc = today - timedelta(days=90)
        elif selected_period == "Past Year":
            from_date_calc = today - timedelta(days=365)
        
        from_date_str = from_date_calc.strftime("%Y-%m-%d")
        to_date_str = today.strftime("%Y-%m-%d")
        filter_info = f"Showing data for {selected_period.lower()} ({from_date_calc} to {today})"

    # Display current filter status
    if filter_type == "Show All Data":
        st.success("📊 " + filter_info)
    else:
        st.info("🔍 " + filter_info)

# Get dashboard metrics
metrics = get_dashboard_metrics(from_date_str, to_date_str)

# Main metrics section
st.subheader("Key Metrics")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="🎯 Sessions Conducted",
        value=metrics["sessions_conducted"],
        help="Total number of counseling sessions conducted in the selected period",
    )

with col2:
    st.metric(
        label="👥 Unique Students Counselled",
        value=metrics["unique_students"],
        help="Number of unique students who had cases registered in the selected period",
    )

with col3:
    st.metric(
        label="📋 New Cases Registered",
        value=metrics["new_cases"],
        help="Number of new counseling cases registered in the selected period",
    )

# Students with no sessions table
st.subheader("Students with Cases but No Sessions")
no_sessions_data = get_students_with_no_sessions(from_date_str, to_date_str)

if no_sessions_data:
    no_sessions_df = pd.DataFrame(
        no_sessions_data,
        columns=[
            "Case ID",
            "Student ID",
            "Student Name",
            "Grade",
            "Section",
            "Reason for Case",
            "Type of Issue",
            "Case Created",
        ],
    )

    st.dataframe(no_sessions_df, use_container_width=True, hide_index=True)

    st.warning(
        f"⚠️ {len(no_sessions_data)} student(s) have registered cases but no counseling sessions yet."
    )
else:
    st.success("✅ All students with cases have had at least one counseling session!")

# Charts section
st.subheader("Data Visualization")

# Create two columns for pie charts
col1, col2 = st.columns(2)

# Issue type breakdown pie chart
with col1:
    st.write("**Issue Type Breakdown**")
    issue_data = get_issue_type_breakdown(from_date_str, to_date_str)

    if issue_data:
        issue_df = pd.DataFrame(issue_data, columns=["Issue Type", "Count"])

        fig_issue = px.pie(
            issue_df,
            values="Count",
            names="Issue Type",
            color_discrete_sequence=px.colors.qualitative.Set3,
        )
        fig_issue.update_layout(
            height=400,
            hoverlabel=dict(bgcolor="white", font_size=16, font_family="Arial"),
        )
        fig_issue.update_traces(
            hovertemplate="<b>%{label}</b><br>Cases: %{value}<br>Percentage: %{percent}<extra></extra>"
        )
        st.plotly_chart(fig_issue, use_container_width=True)
    else:
        st.info("No issue type data available for the selected period.")

# Gender breakdown pie chart
with col2:
    st.write("**Gender Breakdown**")
    gender_data = get_gender_breakdown(from_date_str, to_date_str)

    if gender_data:
        gender_df = pd.DataFrame(gender_data, columns=["Gender", "Count"])

        fig_gender = px.pie(
            gender_df,
            values="Count",
            names="Gender",
            color_discrete_sequence=px.colors.qualitative.Pastel,
        )
        fig_gender.update_layout(
            height=400,
            hoverlabel=dict(bgcolor="white", font_size=16, font_family="Arial"),
        )
        fig_gender.update_traces(
            hovertemplate="<b>%{label}</b><br>Cases: %{value}<br>Percentage: %{percent}<extra></extra>"
        )
        st.plotly_chart(fig_gender, use_container_width=True)
    else:
        st.info("No gender data available for the selected period.")

# Grade breakdown bar chart
st.write("**Cases by Grade**")
grade_data = get_grade_breakdown(from_date_str, to_date_str)

if grade_data:
    grade_df = pd.DataFrame(grade_data, columns=["Grade", "Count"])

    fig_grade = px.bar(
        grade_df, x="Grade", y="Count", color="Count", color_continuous_scale="Blues"
    )
    fig_grade.update_layout(
        height=500,
        xaxis_title="Grade",
        yaxis_title="Number of Cases",
        showlegend=False,
        bargap=0.7,  # Increase spacing between bars even more
        hoverlabel=dict(bgcolor="white", font_size=16, font_family="Arial"),
    )
    fig_grade.update_traces(
        width=0.1,  # Make bars extremely thin
        hovertemplate="<b>Grade %{x}</b><br>Cases: %{y}<extra></extra>",
    )
    st.plotly_chart(fig_grade, use_container_width=True)
else:
    st.info("No grade data available for the selected period.")
