import streamlit as st

st.title("Hello World!")
st.write("This is a test app to verify Streamlit is working.")

if st.button("Click me!"):
    st.balloons()
    st.success("🎉 It's working!")
