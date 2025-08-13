import streamlit as st

# Configure Streamlit
st.set_page_config(
    page_title="Legal Document AI - Test",
    page_icon="⚡",
    layout="wide"
)

# Main app
st.title("⚡ Legal Document AI - Test Version")
st.markdown("**Powered by Neurowaves.AI**")

# Simple interface
st.header("Welcome to Legal Document AI")
st.write("This is a test version for deployment.")

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
