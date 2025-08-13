import streamlit as st
import os
from PIL import Image
import base64

# Configure Streamlit
st.set_page_config(
    page_title="Legal Document AI - Test",
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
st.title("⚡ Legal Document AI - Test Version")
st.markdown("**Powered by Neurowaves.AI**")

# Simple interface
st.header("Welcome to Legal Document AI")
st.write("This is a simplified test version for deployment.")

# API Key status
if OPENAI_API_KEY:
    st.success("✅ OpenAI API Key is configured")
    st.info(f"API Key: {OPENAI_API_KEY[:10]}...")

# Test functionality
if st.button("Test Connection"):
    st.success("🎉 App is working correctly!")
    
# Footer
st.markdown("---")
st.markdown("*Built with Streamlit*")
