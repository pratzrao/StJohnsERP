import streamlit as st
import pandas as pd
from services.db_helper import fetch_sales_records

st.title("View Sales Records")

# Fetch all sales records
sales_records = fetch_sales_records()

if sales_records:
    # Convert to DataFrame for display
    df = pd.DataFrame(sales_records)
    st.dataframe(df, use_container_width=True)
else:
    st.error("No sales records found.")