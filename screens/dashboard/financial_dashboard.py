import streamlit as st
import pandas as pd
import plotly.express as px
from services.db_helper import (
    fetch_total_sales, fetch_total_profit, 
    fetch_defaulter_count_by_grade, fetch_defaulters_list
)

st.title("📊 Financial Dashboard")

# Fetch data
total_sales = fetch_total_sales()
total_profit = fetch_total_profit()
defaulter_counts = fetch_defaulter_count_by_grade()
defaulters_list = fetch_defaulters_list()

# Display total sales and profit as big number metrics
col1, col2 = st.columns(2)
col1.metric("💰 Total Sales (INR)", f"₹{total_sales:,.2f}")
col2.metric("📈 Total Profit (INR)", f"₹{total_profit:,.2f}")

st.markdown("---")

# Defaulter Count by Grade (Bar Chart)
if defaulter_counts:
    df_defaulters = pd.DataFrame(list(defaulter_counts.items()), columns=["Grade", "Defaulters"])
    fig = px.bar(df_defaulters, x="Grade", y="Defaulters", title="Defaulter Count by Grade", text="Defaulters")
    fig.update_traces(marker_color="red", textposition="outside")
    st.plotly_chart(fig)
else:
    st.info("No defaulters recorded.")

st.markdown("---")

# Defaulters List Table
if defaulters_list:
    df_defaulters_list = pd.DataFrame(defaulters_list)
    st.write("### ❌ Defaulters List")
    st.dataframe(df_defaulters_list)
else:
    st.success("No defaulters at this time.")