import streamlit as st

def render():
    st.title("Welcome to AI Conversation Platform")
    st.write("This platform allows you to engage in conversations with an AI, customize your experience, and analyze your interactions.")
    
    if st.session_state.user:
        st.write(f"Welcome back, {st.session_state.user['username']}!")
        st.write("Navigate using the sidebar to start a conversation or view your analytics.")
    else:
        st.write("Please log in or sign up to start using the platform.")
        st.write("You can do this using the sidebar on the left.")