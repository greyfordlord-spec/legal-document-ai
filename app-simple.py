import streamlit as st
import os
import base64
from PIL import Image
import time
import json
import requests

# Configure page
st.set_page_config(
    page_title="Legal Document AI - Powered by Neurowaves.AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="auto"
)

# Constants
DEFAULT_LANGUAGE = "EN"
SUPPORTED_LANGUAGES = {"EN": "English", "DE": "Deutsch"}

# Get API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
if not OPENAI_API_KEY or OPENAI_API_KEY == "your_openai_api_key_here":
    st.error("""
    ⚠️ **OpenAI API Key Required**
    
    Please set your OpenAI API key in Streamlit Cloud:
    1. Go to your app settings
    2. Add secret: OPENAI_API_KEY = your_actual_api_key
    3. Redeploy the app
    """)
    st.stop()

def img_to_base64(image_path):
    """Convert image to base64 with fallback paths."""
    try:
        # Try multiple paths for Streamlit Cloud
        paths_to_try = [
            image_path,
            f"./assets/{os.path.basename(image_path)}",
            f"assets/{os.path.basename(image_path)}",
            os.path.basename(image_path)
        ]
        
        for path in paths_to_try:
            if os.path.exists(path):
                with open(path, "rb") as img_file:
                    return base64.b64encode(img_file.read()).decode()
        
        return None
    except Exception as e:
        st.error(f"Error loading image: {str(e)}")
        return None

def initialize_conversation():
    """Initialize conversation."""
    current_lang = st.session_state.get("current_language", DEFAULT_LANGUAGE)
    if current_lang == "EN":
        return "Hello! I am your Legal Document AI Assistant. How can I help you create legal documents today?"
    else:
        return "Hallo! Ich bin Ihr KI-Assistent für rechtliche Dokumente. Wie kann ich Ihnen heute bei der Erstellung rechtlicher Dokumente helfen?"

def initialize_session_state():
    """Initialize session state."""
    if "current_language" not in st.session_state:
        st.session_state.current_language = DEFAULT_LANGUAGE
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
    if "generated_document" not in st.session_state:
        st.session_state.generated_document = None

def reset_conversation():
    """Reset conversation."""
    st.session_state.conversation_history = []
    st.session_state.generated_document = None

def main():
    """Main application function."""
    initialize_session_state()
    
    # Sidebar
    with st.sidebar:
        st.title("⚡ Legal AI")
        
        # Language selector
        language = st.selectbox(
            "Language / Sprache",
            options=list(SUPPORTED_LANGUAGES.keys()),
            format_func=lambda x: SUPPORTED_LANGUAGES[x],
            key="language_selector"
        )
        
        if language != st.session_state.current_language:
            st.session_state.current_language = language
            reset_conversation()
        
        # Logo
        try:
            logo_path = "assets/Agent_Logo.png"
            logo_base64 = img_to_base64(logo_path)
            if logo_base64:
                st.markdown(f"""
                <div style="text-align: center; margin: 20px 0;">
                    <img src="data:image/png;base64,{logo_base64}" 
                         style="width: 150px; height: auto; border-radius: 10px; box-shadow: 0 0 20px rgba(255,255,255,0.3);">
                </div>
                """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Logo error: {str(e)}")
        
        # Mode selector
        mode = st.radio(
            "Mode",
            ["Chat", "Document Generation"],
            key="mode_selector"
        )
        
        # Reset button
        if st.button("Reset Conversation", key="reset_button"):
            reset_conversation()
            st.rerun()
        
        # Export options
        if st.session_state.generated_document:
            export_format = st.selectbox(
                "Export Format",
                ["docx", "pdf", "txt"],
                key="export_format_selector"
            )
            
            if st.button("Export Document", key="export_button"):
                st.success(f"Document exported as {export_format}")
    
    # Main content
    st.title("⚡ Legal Document AI")
    st.subheader("Powered by Neurowaves.AI")
    
    # Welcome message
    if not st.session_state.conversation_history:
        welcome_msg = initialize_conversation()
        st.session_state.conversation_history.append({"role": "assistant", "content": welcome_msg})
    
    # Display conversation
    for message in st.session_state.conversation_history:
        if message["role"] == "assistant":
            with st.chat_message("assistant", avatar="assets/Agent_icon.png"):
                st.write(message["content"])
        else:
            with st.chat_message("user", avatar="assets/stuser.png"):
                st.write(message["content"])
    
    # Chat input
    if mode == "Chat":
        chat_input = st.chat_input("Ask me anything about legal documents...", key="chat_input_ai_mode")
        if chat_input:
            # Add user message
            st.session_state.conversation_history.append({"role": "user", "content": chat_input})
            
            # Simple AI response (you can enhance this)
            ai_response = f"I understand you're asking about: {chat_input}. This is a simplified response. For full functionality, please check the complete version."
            st.session_state.conversation_history.append({"role": "assistant", "content": ai_response})
            st.rerun()
    
    elif mode == "Document Generation":
        chat_input = st.chat_input("Tell me what document you need...", key="chat_input_doc_mode")
        if chat_input:
            st.session_state.conversation_history.append({"role": "user", "content": chat_input})
            
            # Document generation response
            doc_response = f"I'll help you create a document about: {chat_input}. This is a simplified response. For full functionality, please check the complete version."
            st.session_state.conversation_history.append({"role": "assistant", "content": doc_response})
            st.rerun()
    
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Generate Documents", key="documents_button"):
            st.info("Document generation feature - simplified version")
    
    with col2:
        if st.button("View History", key="history_button"):
            st.info("History feature - simplified version")

if __name__ == "__main__":
    main()
