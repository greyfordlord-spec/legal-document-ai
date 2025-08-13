import streamlit as st
import os
from typing import Optional
from core.conversation import ConversationManager
from core.document_gen import DocumentGenerator
from utils.export import DocumentExporter
from config.settings import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES, STREAMLIT_THEME
from config.ui_translations import get_ui_text, get_page_config
import logging
from PIL import Image, ImageEnhance
import time
import json
import requests
import base64

# Configure logging
logging.basicConfig(level=logging.INFO)

# Constants
NUMBER_OF_MESSAGES_TO_DISPLAY = 20

# Retrieve and validate API key (with Streamlit Cloud support)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
if not OPENAI_API_KEY or OPENAI_API_KEY == "your_openai_api_key_here":
    st.error("""
    ⚠️ **OpenAI API Key Required**
    
    Please set your OpenAI API key in Streamlit Cloud:
    1. Go to your app settings
    2. Add secret: OPENAI_API_KEY = your_actual_api_key
    3. Redeploy the app
    
    Or set it as an environment variable.
    """)
    st.stop()

# Streamlit Page Configuration
st.set_page_config(
    page_title="Legal Document AI - Powered by Neurowaves.AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        "Get help": "https://neurowaves.ai",
        "Report a bug": "https://neurowaves.ai",
        "About": """
            ## Legal Document AI - Powered by Neurowaves.AI
            ### Advanced AI Legal Assistant

            **Powered by**: Neurowaves.AI - Advanced AI Solutions

            The AI Assistant aims to provide intelligent legal document creation,
            generate professional legal documents, and answer questions about legal processes.
            The system has been trained on legal document templates and best practices.
        """
    }
)

# Streamlit Title - Will be updated dynamically in main function
# Removed duplicate title - now handled dynamically in main() function

def img_to_base64(image_path):
    """Convert image to base64 with fallback paths for Streamlit Cloud."""
    try:
        # Try the original path first
        if os.path.exists(image_path):
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
        
        # Fallback paths for Streamlit Cloud deployment
        fallback_paths = [
            f"./assets/{os.path.basename(image_path)}",
            f"assets/{os.path.basename(image_path)}",
            os.path.basename(image_path)
        ]
        
        for fallback_path in fallback_paths:
            if os.path.exists(fallback_path):
                with open(fallback_path, "rb") as img_file:
                    return base64.b64encode(img_file.read()).decode()
        
        logging.error(f"Image not found at any path: {image_path}")
        return None
        
    except Exception as e:
        logging.error(f"Error converting image to base64: {str(e)}")
        return None

def long_running_task(duration):
    """
    Simulates a long-running operation.

    Parameters:
    - duration: int, duration of the task in seconds

    Returns:
    - str: Completion message
    """
    time.sleep(duration)
    return "Long-running operation completed."

def load_and_enhance_image(image_path, enhance=False):
    """
    Load and optionally enhance an image.

    Parameters:
    - image_path: str, path of the image
    - enhance: bool, whether to enhance the image or not

    Returns:
    - img: PIL.Image.Image, (enhanced) image
    """
    try:
        img = Image.open(image_path)
        if enhance:
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.8)
        return img
    except Exception as e:
        logging.error(f"Error loading image {image_path}: {str(e)}")
        return None

def initialize_conversation():
    """
    Initialize the conversation history with only the initial assistant message.

    Returns:
    - list: Initialized conversation history.
    """
    # Get current language from session state or use default
    current_lang = st.session_state.get("current_language", DEFAULT_LANGUAGE)
    assistant_message = f"Hello! I am your {get_ui_text('chat_title', current_lang)}. How can I help you create legal documents today?"

    conversation_history = [
        {"role": "assistant", "content": assistant_message}
    ]
    return conversation_history

def initialize_session_state():
    """Initialize session state variables."""
    if "conversation_manager" not in st.session_state:
        st.session_state.conversation_manager = ConversationManager(DEFAULT_LANGUAGE)
    
    if "current_language" not in st.session_state:
        st.session_state.current_language = DEFAULT_LANGUAGE
    
    if "generated_document" not in st.session_state:
        st.session_state.generated_document = None
    
    if "document_type" not in st.session_state:
        st.session_state.document_type = None
    
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []

def reset_conversation():
    """Reset the conversation and start over."""
    st.session_state.conversation_manager.reset_conversation()
    st.session_state.generated_document = None
    st.session_state.document_type = None
    st.session_state.conversation_history = initialize_conversation()

def on_chat_submit(chat_input):
    """
    Handle chat input submissions and interact with the AI.

    Parameters:
    - chat_input (str): The chat input from the user.

    Returns:
    - None: Updates the chat history in Streamlit's session state.
    """
    user_input = chat_input.strip()

    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = initialize_conversation()

    # Add user message to conversation history (for display)
    st.session_state.conversation_history.append({"role": "user", "content": user_input})

    try:
        # Process user message through conversation manager
        response, is_complete = st.session_state.conversation_manager.process_user_message(user_input)
        
        # Add AI response to conversation history (for display)
        st.session_state.conversation_history.append({"role": "assistant", "content": response})
        
        # If document generation is complete, store the document
        if is_complete:
            # Extract document from response
            lines = response.split('\n')
            document_start = False
            document_lines = []
            
            for line in lines:
                if "Here's your generated" in line:
                    document_start = True
                    continue
                elif document_start and "You can now export" in line:
                    break
                elif document_start:
                    document_lines.append(line)
            
            if document_lines:
                st.session_state.generated_document = '\n'.join(document_lines)
                st.session_state.document_type = st.session_state.conversation_manager.get_current_document_type()

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        st.error(f"Error: {str(e)}")

def main():
    """
    Display the main interface and handle the chat interface.
    """
    initialize_session_state()

    # Initialize conversation if not exists
    if 'conversation_history' not in st.session_state or not st.session_state.conversation_history:
        st.session_state.conversation_history = initialize_conversation()

    # Insert custom CSS for glowing effect
    st.markdown(
        """
        <style>
        .cover-glow {
            width: 100%;
            height: auto;
            padding: 3px;
            box-shadow: 
                0 0 5px #ffffff,
                0 0 10px #ffffff,
                0 0 15px #ffffff,
                0 0 20px #ffffff,
                0 0 25px #ffffff,
                0 0 30px #ffffff,
                0 0 35px #ffffff;
            position: relative;
            z-index: -1;
            border-radius: 45px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Load and display sidebar image (using Agent Logo)
    img_path = "assets/Agent_Logo.png"
    img_base64 = img_to_base64(img_path)
    if img_base64:
        st.sidebar.markdown(
            f'<img src="data:image/png;base64,{img_base64}" style="width: 100%; height: auto; border-radius: 12px;" class="cover-glow">',
            unsafe_allow_html=True,
        )
    else:
        st.sidebar.markdown(
            """
            <div style="text-align: center; padding: 1rem 0;">
                <div style="font-size: 4rem; margin-bottom: 0.5rem;">⚖️</div>
                <h2 style="margin: 0; color: #1f77b4;">Legal Document AI</h2>
                <p style="margin: 0.5rem 0 0 0; color: #6c757d; font-size: 0.9rem;">Your AI Legal Assistant</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.sidebar.markdown("---")

    # Language selection - First show the title
    st.sidebar.markdown(f"#### 🌍 {get_ui_text('language', st.session_state.current_language)}")
    
    # Then define the language variable
    language = st.sidebar.selectbox(
        "Select Language:",
        options=list(SUPPORTED_LANGUAGES.keys()),
        format_func=lambda x: SUPPORTED_LANGUAGES[x],
        index=list(SUPPORTED_LANGUAGES.keys()).index(st.session_state.current_language),
        label_visibility="collapsed",
        key="language_selector"
    )
    
    if language != st.session_state.current_language:
        st.session_state.current_language = language
        st.session_state.conversation_manager = ConversationManager(language)
        reset_conversation()

    # Update page title dynamically based on selected language
    st.title(get_ui_text("page_title", language))

    # Sidebar for Mode Selection
    mode = st.sidebar.radio(
        get_ui_text("mode_selection", language), 
        options=[get_ui_text("document_creation", language), get_ui_text("chat_with_ai", language)], 
        index=0,
        key="mode_selector"
    )

    # Reset button
    if st.sidebar.button(f"🔄 {get_ui_text('reset_conversation', language)}", use_container_width=True, key="reset_button"):
        reset_conversation()
        st.rerun()

    # Export section (only show if document is generated)
    if st.session_state.generated_document:
        st.sidebar.markdown("---")
        st.sidebar.markdown(f"""
        <div style="background: linear-gradient(135deg, #059669 0%, #10b981 100%); color: white; padding: 1rem; border-radius: 12px; margin-bottom: 1rem; text-align: center;">
            <h4 style="margin: 0 0 0.5rem 0; color: white;">📄 {get_ui_text('export_document', language)}</h4>
            <p style="margin: 0; opacity: 0.9; font-size: 0.9rem; color: white;">{get_ui_text('document_ready', language)}</p>
        </div>
        """, unsafe_allow_html=True)
        
        export_format = st.sidebar.selectbox(
            get_ui_text("export_format", language),
            options=["docx", "pdf"],
            index=0,
            label_visibility="collapsed",
            key="export_format_selector"
        )
        
        if st.sidebar.button(f"💾 {get_ui_text('export_document', language)}", use_container_width=True, key="export_button"):
            exporter = DocumentExporter()
            filepath = exporter.export_document(
                st.session_state.generated_document,
                st.session_state.document_type,
                export_format,
                st.session_state.current_language
            )
            
            if filepath:
                with open(filepath, "rb") as file:
                    st.sidebar.download_button(
                        label=f"📥 Download {export_format.upper()}",
                        data=file.read(),
                        file_name=os.path.basename(filepath),
                        mime="application/octet-stream",
                        use_container_width=True
                    )
                st.sidebar.success(get_ui_text("export_success", language))
            else:
                st.sidebar.error(get_ui_text("export_failed", language))

    st.sidebar.markdown("---")

    # Agent Panel
    st.sidebar.markdown(f"### 🤖 {get_ui_text('ai_agent_panel', language)}")
    st.sidebar.markdown(f"*{get_ui_text('your_legal_assistant', language)}*")
    
    # File Management Section
    st.sidebar.markdown(f"#### 📁 {get_ui_text('file_management', language)}")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button(f"📄 {get_ui_text('documents', language)}", use_container_width=True, key="documents_button"):
            st.info(get_ui_text("documents_feature_coming", language))
    with col2:
        if st.button(f"💬 {get_ui_text('history', language)}", use_container_width=True, key="history_button"):
            st.info(get_ui_text("history_feature_coming", language))
    
    # Document Capabilities Section
    st.sidebar.markdown(f"#### ⚖️ {get_ui_text('document_capabilities', language)}")
    
    # Create a simple grid layout
    capabilities_data = [
        ("📋", get_ui_text("contracts", language), "blue"),
        ("🔒", get_ui_text("ndas", language), "green"),
        ("🏠", get_ui_text("leases", language), "orange"),
        ("📝", get_ui_text("agreements", language), "red"),
        ("📜", get_ui_text("wills_trusts", language), "purple"),
        ("🏢", get_ui_text("incorporation", language), "indigo")
    ]
    
    # Display capabilities in a grid
    cols = st.sidebar.columns(2)
    for idx, (icon, name, color) in enumerate(capabilities_data):
        with cols[idx % 2]:
            st.markdown(f"""
            <div style="text-align: center; padding: 0.5rem; background: rgba(255,255,255,0.1); 
                        border-radius: 8px; margin: 0.2rem 0;">
                <div style="font-size: 1.5rem;">{icon}</div>
                <div style="font-size: 0.8rem; color: #e2e8f0;">{name}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # About Section
    st.sidebar.markdown(f"#### ℹ️ {get_ui_text('about_agent', language)}")
    st.sidebar.info(get_ui_text("about_description", language))

    st.sidebar.markdown("---")



    # Load and display Neurowaves.AI logo with custom styling
    img_path = "assets/neurowaves_logo.png"
    img_base64 = img_to_base64(img_path)
    if img_base64:
        st.sidebar.markdown(
            f"""
            <div style="text-align: center; margin-top: -5rem; margin-bottom: -1rem;">
                <img src="data:image/png;base64,{img_base64}" style="width: 140%; height: auto; border-radius: 12px; margin-left: -20%;">
                <p style="margin: -1.5rem 0 0 0; color: #94a3b8; font-size: 1.1rem; font-weight: 500;">⚡ Powered by Neurowaves AI</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        # Fallback to text-based Neurowaves.AI branding
        st.sidebar.markdown(
            """
            <div style="text-align: center; padding: 1rem 0; margin-top: -5rem;">
                <div style="font-size: 2rem; margin-bottom: 0.1rem; color: #ffffff;">⚡</div>
                <h3 style="margin: 0; color: #ffffff; font-weight: 700;">NEUROWAVES.AI</h3>
                <p style="margin: -1.5rem 0 0 0; color: #94a3b8; font-size: 1.1rem; font-weight: 500;">⚡ Powered by Neurowaves AI</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if mode == get_ui_text("chat_with_ai", language):
        chat_input = st.chat_input(get_ui_text("chat_placeholder", language), key="chat_input_ai_mode")
        if chat_input:
            on_chat_submit(chat_input)

        # Display chat history with avatar images
        for message in st.session_state.conversation_history[-NUMBER_OF_MESSAGES_TO_DISPLAY:]:
            role = message["role"]
            avatar_image = "assets/Agent_icon.png" if role == "assistant" else "assets/stuser.png" if role == "user" else None
            with st.chat_message(role, avatar=avatar_image):
                st.markdown(message["content"])

    else:
        # Document Creation Mode
        chat_input = st.chat_input("💭 Ask me anything about legal documents, or let's start creating one...", key="chat_input_doc_mode")
        if chat_input:
            # Process the chat input through the conversation manager
            on_chat_submit(chat_input)
            st.rerun()  # Rerun to refresh the display

        # Display chat messages with avatar images
        if st.session_state.conversation_history:
            for message in st.session_state.conversation_history:
                role = message["role"]
                avatar_image = "assets/Agent_icon.png" if role == "assistant" else "assets/stuser.png" if role == "user" else None
                with st.chat_message(role, avatar=avatar_image):
                    st.markdown(message["content"])

        # Enhanced progress display with proper styling
        if st.session_state.conversation_manager.get_current_document_type():
            current_doc = st.session_state.conversation_manager.get_current_document_type()
            collected_data = st.session_state.conversation_manager.get_collected_data()
            
            st.markdown("""
            <div style="background: rgba(255, 255, 255, 0.02); 
                        border-radius: 20px; 
                        padding: 2rem; 
                        margin: 1rem 0; 
                        border: 1px solid rgba(255, 255, 255, 0.1);
                        backdrop-filter: blur(10px);
                        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);">
                <div style="text-align: center; margin-bottom: 1.5rem;">
                    <h3 style="color: #cbd5e1; margin: 0; font-weight: 600;">📋 Document Creation Progress</h3>
                </div>
                <div style="background: #f1f5f9; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
                    <strong style="color: #1f2937;">Document Type:</strong> 
                    <span style="color: #374151; margin-left: 0.5rem;">{}</span>
                </div>
                <div style="background: #f1f5f9; padding: 1rem; border-radius: 10px;">
                    <strong style="color: #1f2937;">Collected Information:</strong>
                    <div style="margin-top: 0.5rem;">
            """.format(current_doc), unsafe_allow_html=True)
            
            for key, value in collected_data.items():
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #e5e7eb;">
                    <span style="color: #374151; font-weight: 500;">{key}:</span>
                    <span style="color: #6b7280;">{value}</span>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div></div></div>', unsafe_allow_html=True)

if __name__ == "__main__":
    # Check for required environment variables
    if not os.getenv("OPENAI_API_KEY"):
        st.error("""
        ⚠️ **OpenAI API Key Required**
        
        Please set your OpenAI API key in a `.env` file:
        ```
        OPENAI_API_KEY=your_api_key_here
        ```
        
        Or set it as an environment variable.
        """)
        st.stop()
    
    main()


