import streamlit as st

st.title("🔗 Shareable Links")
st.write("Manage and share public forms and resources.")

# Get current URL info
try:
    import os
    base_url = "https://stjohnserp.streamlit.app"
    if 'STREAMLIT_SERVER_PORT' in os.environ:
        port = os.environ['STREAMLIT_SERVER_PORT']
        base_url = f"http://localhost:{port}"
    elif any(key.startswith('STREAMLIT') for key in os.environ.keys()):
        base_url = "https://stjohnserp.streamlit.app"
    if st.session_state.get("deployed_url"):
        base_url = st.session_state["deployed_url"]
except Exception as e:
    base_url = "https://stjohnserp.streamlit.app"

# Shareable Links List
shareable_links = [
    {
        "name": "Public Survey Form",
        "description": "Simple Yes/No survey form accessible to anyone without login",
        "url_path": "/?page=public_survey",
        "icon": "📝",
        "data_key": "survey_responses"
    }
    # Future links can be added here
]

# Display each shareable link
for link in shareable_links:
    with st.container():
        st.subheader(f"{link['icon']} {link['name']}")
        
        # Generate full URL
        full_url = f"{base_url}{link['url_path']}"
        
        # Display URL in plain text
        st.text(full_url)
        
        # Action buttons
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button("📋 Copy", key=f"copy_{link['name']}"):
                # JavaScript to copy URL to clipboard
                js_code = f"""
                <script>
                navigator.clipboard.writeText('{full_url}').then(function() {{
                    console.log('URL copied to clipboard');
                }}).catch(function(err) {{
                    console.error('Failed to copy: ', err);
                }});
                </script>
                """
                st.components.v1.html(js_code, height=0)
                st.success("Link copied!")
        
        with col2:
            if st.button("🔗 Open", key=f"open_{link['name']}"):
                js_code = f"""
                <script>
                window.open('{full_url}', '_blank');
                </script>
                """
                st.components.v1.html(js_code, height=0)
        
        with col3:
            st.write(f"*{link['description']}*")
        
        # Show response data if available
        if link.get('data_key') and link['data_key'] in st.session_state:
            data = st.session_state[link['data_key']]
            if data:
                with st.expander(f"📊 View {link['name']} Responses ({len(data)} total)"):
                    # Quick stats
                    if link['data_key'] == 'survey_responses':
                        yes_count = sum(1 for resp in data if resp["response"] == "Yes")
                        no_count = sum(1 for resp in data if resp["response"] == "No")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total", len(data))
                        with col2:
                            st.metric("Yes", yes_count)
                        with col3:
                            st.metric("No", no_count)
                        
                        # Individual responses
                        if st.checkbox(f"Show all responses", key=f"show_all_{link['name']}"):
                            for i, resp in enumerate(data, 1):
                                st.write(f"**{i}.** {resp['name']} - {resp['response']} ({resp['timestamp']})")
                    
                    # Clear data button
                    if st.button(f"🗑️ Clear Data", key=f"clear_{link['name']}", type="secondary"):
                        st.session_state[link['data_key']] = []
                        st.success("Data cleared!")
                        st.rerun()
            else:
                st.info(f"No responses yet for {link['name']}")
        
        st.divider()

# URL Configuration (collapsed by default)
with st.expander("⚙️ URL Configuration"):
    custom_url = st.text_input(
        "Override base URL:",
        value=base_url,
        help="Leave as default unless you need to override the auto-detected URL"
    )
    
    if st.button("Update URL"):
        st.session_state["deployed_url"] = custom_url
        st.success("URL updated!")
        st.rerun()