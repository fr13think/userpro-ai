import streamlit as st
from flask import Flask
from flask_login import LoginManager
from backend.auth import login_manager
from .pages import home, user_profile, conversation, dashboard
from ai_platform.config import Config
from backend.api import api as api_blueprint
from utils.logger import setup_logger

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(api_blueprint, url_prefix='/api')

    setup_logger(app)
    login_manager.init_app(app)

    @app.route('/')
    def streamlit_view():
        return st.script_runner.get_scriptrunner().get_script_run_ctx().streamlit_script_run_ctx.main_script_run_ctx.get_main_script_path()

    return app

def run_app():
    st.set_page_config(page_title="AI Conversation Platform", layout="wide")
    
    if 'user' not in st.session_state:
        st.session_state.user = None

    pages = {
        "Home": home,
        "User Profile": user_profile,
        "Conversation": conversation,
        "Dashboard": dashboard
    }
    
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(pages.keys()))
    
    page = pages[selection]
    page.app()