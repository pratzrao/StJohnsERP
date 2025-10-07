import streamlit as st

st.title("📎 Shareable Links")
st.write("This page contains shareable links for public forms and resources.")

# Get current URL info
try:
    # For local development
    base_url = "http://localhost:8501"
    
    # Check if we can detect the actual URL (works in some deployments)
    import os
    if 'STREAMLIT_SERVER_PORT' in os.environ:
        port = os.environ['STREAMLIT_SERVER_PORT']
        base_url = f"http://localhost:{port}"
    
    # For deployed apps, users will need to replace this with their actual URL
    if st.session_state.get("deployed_url"):
        base_url = st.session_state["deployed_url"]
        
except Exception as e:
    base_url = "http://localhost:8501"

# Allow users to set their deployed URL
st.subheader("⚙️ URL Configuration")
custom_url = st.text_input(
    "Enter your app's URL (for deployed apps):",
    value=base_url,
    help="For local testing use: http://localhost:8501\nFor deployed apps, enter your Streamlit app URL"
)

if st.button("Save URL"):
    st.session_state["deployed_url"] = custom_url
    st.success("URL saved!")
    st.rerun()

# Use the custom URL or default
final_base_url = custom_url if custom_url else base_url

st.divider()

# Public Survey Form Link
st.subheader("📝 Public Survey Form")
survey_url = f"{final_base_url}/?page=public_survey"

col1, col2 = st.columns([3, 1])

with col1:
    st.code(survey_url, language=None)

with col2:
    if st.button("📋 Copy Link", key="copy_survey"):
        # Note: This will copy to clipboard in some browsers
        st.write("Link copied!")
        
st.warning("⚠️ **IMPORTANT:** Make sure to use the EXACT URL above including `?page=public_survey`")

st.write("**Description:** Public survey form that anyone can access without login.")
st.write("**Features:**")
st.write("- ✅ No authentication required")
st.write("- ✅ Clean, Google Forms-like interface") 
st.write("- ✅ Saves responses to CSV file")
st.write("- ✅ Mobile-friendly design")

st.info("💡 **Copy the full URL above and paste it in a NEW browser tab to test**")

# Testing Instructions
st.divider()
st.subheader("🧪 Testing Instructions")

with st.expander("How to test locally"):
    st.write("""
    **Step 1: Start your Streamlit app**
    ```bash
    cd "/Users/pratiksharao/Counselling Software/StJohnsERP"
    streamlit run main.py
    ```
    
    **Step 2: Test the shareable link**
    1. Copy the EXACT survey URL above (it should include `?page=public_survey`)
    2. Open a NEW browser tab/window (important!)
    3. Paste the URL and press Enter
    4. You should see ONLY the survey form (no login, no navigation)
    
    **⚠️ IMPORTANT URL FORMAT:**
    - ✅ CORRECT: `http://localhost:8501/?page=public_survey`
    - ❌ WRONG: `http://localhost:8501/public_survey`
    - ❌ WRONG: `http://localhost:8501/public_survey.py`
    
    **Step 3: Test incognito/private browsing**
    1. Open an incognito/private browser window
    2. Paste the survey URL (with ?page=public_survey)
    3. Verify it works without any authentication
    
    **Step 4: Test form submission**
    1. Fill out the form and submit
    2. Check that CSV file is created at:
       `/Users/pratiksharao/Counselling Software/StJohnsERP/survey_responses.csv`
    """)

with st.expander("Troubleshooting"):
    st.write("""
    **If the link doesn't work:**
    - Make sure your Streamlit app is running
    - Check that the port number matches (usually 8501)
    - Try refreshing the page
    
    **If you see the login page instead:**
    - Make sure the URL includes `?page=public_survey`
    - Check for typos in the URL
    
    **For deployed apps:**
    - Replace `localhost:8501` with your actual Streamlit app URL
    - Example: `https://your-app.streamlit.app/?page=public_survey`
    """)

# Quick Test Button
st.divider()
st.subheader("⚡ Quick Test")
if st.button("🧪 Open Survey in New Tab", type="primary"):
    st.write(f"Opening: {survey_url}")
    st.write("Copy the URL above and paste it in a new browser tab to test.")
    
    # JavaScript to open in new tab (may not work in all environments)
    js_code = f"""
    <script>
    window.open('{survey_url}', '_blank');
    </script>
    """
    st.components.v1.html(js_code, height=0)

# CSV File Location
st.divider()
st.subheader("📁 Data File Location")
csv_path = "/Users/pratiksharao/Counselling Software/StJohnsERP/survey_responses.csv"
st.code(csv_path, language=None)

# Check if CSV file exists
import os
if os.path.exists(csv_path):
    st.success("✅ CSV file exists")
    
    # Show file size and last modified
    file_stats = os.stat(csv_path)
    file_size = file_stats.st_size
    import datetime
    last_modified = datetime.datetime.fromtimestamp(file_stats.st_mtime)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("File Size", f"{file_size} bytes")
    with col2:
        st.metric("Last Modified", last_modified.strftime("%Y-%m-%d %H:%M:%S"))
        
    # Option to view CSV contents (for admins)
    if st.checkbox("📊 View CSV Contents"):
        try:
            import pandas as pd
            df = pd.read_csv(csv_path)
            st.dataframe(df)
        except Exception as e:
            st.error(f"Error reading CSV: {e}")
else:
    st.info("ℹ️ CSV file will be created when first response is submitted")