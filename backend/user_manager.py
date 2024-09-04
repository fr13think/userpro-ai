import streamlit as st
from backend.security import check_password, hash_password
import logging

class UserManager:
    def __init__(self):
        if 'users' not in st.session_state:
            st.session_state.users = {}
        logging.info("UserManager initialized")

    def create_user(self, username, email, password):
        if username in st.session_state.users:
            logging.warning(f"Attempt to create duplicate user: {username}")
            return False
        hashed_password = hash_password(password)
        st.session_state.users[username] = {"email": email, "password": hashed_password, "preferences": {}}
        logging.info(f"New user created: {username}")
        return True

    def get_user(self, username):
        user = st.session_state.users.get(username)
        if user:
            logging.info(f"Retrieved user: {username}")
        else:
            logging.warning(f"Attempt to retrieve non-existent user: {username}")
        return user

    def authenticate(self, username, password):
        user = self.get_user(username)
        if user and check_password(password, user['password']):
            logging.info(f"User authenticated: {username}")
            return True
        logging.warning(f"Failed authentication attempt for user: {username}")
        return False

    def update_user_preferences(self, username, preferences):
        if username in st.session_state.users:
            st.session_state.users[username]["preferences"] = preferences
            logging.info(f"Updated preferences for user: {username}")
            return True
        logging.warning(f"Attempt to update preferences for non-existent user: {username}")
        return False