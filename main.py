import streamlit as st
from frontend.pages import home, user_profile, conversation, dashboard, prompt_management
from backend.user_manager import UserManager
from backend.conversation_engine import ConversationEngine
from backend.llama_model import LlamaModel
from backend.groq_client import GroqClient
from backend.analytics_engine import AnalyticsEngine
from backend.prompt_manager import PromptManager
from utils.config import load_config
from utils.database import get_db
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load configuration
config = load_config()

# Initialize backend components
llama_model = LlamaModel(config['llama_model_path'])
groq_client = GroqClient(config['groq_api_key'])
conversation_engine = ConversationEngine(llama_model, groq_client)
user_manager = UserManager()
analytics_engine = AnalyticsEngine()
db = next(get_db())
prompt_manager = PromptManager(db)

# Streamlit app
st.set_page_config(page_title="AI Conversation Platform", layout="wide")

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = None

# Sidebar for authentication
if st.session_state.user is None:
    st.sidebar.title("Authentication")
    auth_option = st.sidebar.selectbox("Choose an option", ["Login", "Sign Up"])
    
    if auth_option == "Login":
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            if user_manager.authenticate(username, password):
                st.session_state.user = user_manager.get_user(username)
                st.success("Logged in successfully!")
            else:
                st.error("Invalid username or password")
    else:
        username = st.sidebar.text_input("Username")
        email = st.sidebar.text_input("Email")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Sign Up"):
            if user_manager.create_user(username, email, password):
                st.success("User created successfully. Please log in.")
            else:
                st.error("Username already exists")

# Main content
if st.session_state.user:
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "User Profile", "Conversation", "Dashboard", "Prompt Management"])

    if page == "Home":
        home.render()
    elif page == "User Profile":
        user_profile.render(user_manager)
    elif page == "Conversation":
        conversation.render(conversation_engine, prompt_manager)
    elif page == "Dashboard":
        dashboard.render(analytics_engine)
    elif page == "Prompt Management":
        prompt_management.render(prompt_manager)

    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.experimental_rerun()
else:
    home.render()

if __name__ == "__main__":
    st.write("Running AI Conversation Platform")