import streamlit as st
import csv
import os
from datetime import datetime

# Configure the page to look more like a standalone form
st.set_page_config(
    page_title="Survey Form",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit style elements for a cleaner look
hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("📝 Survey Form")
st.write("Please take a moment to complete this quick survey.")

# Create a simple yes/no question
response = st.selectbox(
    "Please select your response:",
    ["", "Yes", "No"],
    placeholder="Choose an option..."
)

# Optional: Add name field
name = st.text_input("Name (Optional):", placeholder="Enter your name")

# Submit button
if st.button("Submit Response"):
    if response and response != "":
        # Create CSV file path
        csv_file_path = "/Users/pratiksharao/Counselling Software/StJohnsERP/survey_responses.csv"
        
        # Prepare data
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response_data = [timestamp, name if name else "Anonymous", response]
        
        # Check if file exists, if not create with headers
        file_exists = os.path.isfile(csv_file_path)
        
        try:
            with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write headers if file is new
                if not file_exists:
                    writer.writerow(["Timestamp", "Name", "Response"])
                
                # Write the response
                writer.writerow(response_data)
            
            st.success("✅ Thank you! Your response has been recorded.")
            st.balloons()
            
        except Exception as e:
            st.error(f"❌ Error saving response: {e}")
    else:
        st.warning("⚠️ Please select a response before submitting.")

# Optional: Show some stats (without revealing individual responses)
if st.checkbox("Show response statistics"):
    csv_file_path = "/Users/pratiksharao/Counselling Software/StJohnsERP/survey_responses.csv"
    
    if os.path.isfile(csv_file_path):
        try:
            with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                responses = list(reader)[1:]  # Skip header
                
                if responses:
                    yes_count = sum(1 for row in responses if len(row) > 2 and row[2] == "Yes")
                    no_count = sum(1 for row in responses if len(row) > 2 and row[2] == "No")
                    total = yes_count + no_count
                    
                    st.write("### Response Summary")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Yes", yes_count)
                    with col2:
                        st.metric("No", no_count)
                    with col3:
                        st.metric("Total", total)
                        
                    if total > 0:
                        st.write(f"**Yes: {yes_count/total*100:.1f}%** | **No: {no_count/total*100:.1f}%**")
                else:
                    st.write("No responses yet.")
        except Exception as e:
            st.error(f"Error reading responses: {e}")
    else:
        st.write("No responses yet.")