import streamlit as st
from frontend.pages import home, user_profile, conversation, dashboard
from backend.user_manager import UserManager
from backend.conversation_engine import ConversationEngine
from backend.llama_model import LlamaModel
from backend.groq_client import GroqClient
from backend.analytics_engine import AnalyticsEngine
from backend.security import check_password, hash_password
from utils.config import load_config

# Load configuration
config = load_config()

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = None

# Initialize backend components
llama_model = LlamaModel(config['llama_model_path'])
groq_client = GroqClient(config['groq_api_key'])
conversation_engine = ConversationEngine(llama_model, groq_client)
user_manager = UserManager()
analytics_engine = AnalyticsEngine()

# Streamlit app
st.set_page_config(page_title="AI Conversation Platform", layout="wide")

# Authentication
if st.session_state.user is None:
    choice = st.sidebar.radio("Login/Signup", ["Login", "Sign Up"])
    if choice == "Login":
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            if user_manager.authenticate(username, password):
                st.session_state.user = user_manager.get_user(username)
                st.success("Logged in successfully")
            else:
                st.error("Invalid username or password")
    else:
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        email = st.sidebar.text_input("Email")
        if st.sidebar.button("Sign Up"):
            if user_manager.create_user(username, email, password):
                st.success("User created successfully. Please log in.")
            else:
                st.error("Username already exists")

# Sidebar navigation
if st.session_state.user:
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "User Profile", "Conversation", "Dashboard"])

    # Render the selected page
    if page == "Home":
        home.render()
    elif page == "User Profile":
        user_profile.render(user_manager)
    elif page == "Conversation":
        conversation.render(conversation_engine)
    elif page == "Dashboard":
        dashboard.render(analytics_engine)

    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.experimental_rerun()
