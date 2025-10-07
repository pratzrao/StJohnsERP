import streamlit as st
from datetime import datetime

# Configure the page to look more like a standalone form
st.set_page_config(
    page_title="Survey Form",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="collapsed",
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

st.title("Survey Form")
st.write("Please take a moment to complete this quick survey.")

# Create a simple yes/no question
response = st.selectbox(
    "Please select your response:", ["", "Yes", "No"], placeholder="Choose an option..."
)

# Optional: Add name field
name = st.text_input("Name (Optional):", placeholder="Enter your name")

# Initialize survey responses in session state
if "survey_responses" not in st.session_state:
    st.session_state.survey_responses = []

# Submit button
if st.button("Submit Response"):
    if response and response != "":
        # Prepare data
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response_data = {
            "timestamp": timestamp,
            "name": name if name else "Anonymous",
            "response": response,
        }

        try:
            # Add to session state (persistent across the session)
            st.session_state.survey_responses.append(response_data)

            st.success("✅ Thank you! Your response has been recorded.")
            st.balloons()

        except Exception as e:
            st.error(f"❌ Error saving response: {e}")
    else:
        st.warning("⚠️ Please select a response before submitting.")

# Optional: Show some stats (without revealing individual responses)
if st.checkbox("Show response statistics"):
    responses = st.session_state.survey_responses

    if responses:
        yes_count = sum(1 for resp in responses if resp["response"] == "Yes")
        no_count = sum(1 for resp in responses if resp["response"] == "No")
        total = len(responses)

        st.write("### Response Summary")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Yes", yes_count)
        with col2:
            st.metric("No", no_count)
        with col3:
            st.metric("Total", total)

        if total > 0:
            yes_pct = (yes_count / total * 100) if total > 0 else 0
            no_pct = (no_count / total * 100) if total > 0 else 0
            st.write(f"**Yes: {yes_pct:.1f}%** | **No: {no_pct:.1f}%**")
    else:
        st.write("No responses yet.")
