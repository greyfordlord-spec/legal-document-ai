import streamlit as st
import os

# Configure Streamlit
st.set_page_config(
    page_title="Legal Document AI",
    page_icon="⚡",
    layout="wide"
)

# Check for API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("""
    ⚠️ **OpenAI API Key Required**
    
    Please set your OpenAI API key in Streamlit Cloud:
    1. Go to your app settings
    2. Add secret: OPENAI_API_KEY = your_actual_api_key
    3. Redeploy the app
    """)
    st.stop()

# Main app
st.title("⚡ Legal Document AI")
st.markdown("**Powered by Neurowaves.AI**")

# Simple interface
st.header("Welcome to Legal Document AI")
st.write("This is a simplified version for deployment.")

# API Key status
if OPENAI_API_KEY:
    st.success("✅ OpenAI API Key is configured")
    st.info(f"API Key: {OPENAI_API_KEY[:10]}...")

# Test functionality
if st.button("Test Connection"):
    st.success("🎉 App is working correctly!")
    
# Simple form
with st.form("test_form"):
    name = st.text_input("Enter your name:")
    submitted = st.form_submit_button("Submit")
    if submitted and name:
        st.write(f"Hello, {name}! The app is working.")

# Footer
st.markdown("---")
st.markdown("*Built with Streamlit*")


