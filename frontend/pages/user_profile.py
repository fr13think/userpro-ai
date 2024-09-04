import streamlit as st

def render(user_manager):
    st.title("User Profile")

    if st.session_state.user:
        username = st.session_state.user['username']
        user = user_manager.get_user(username)
        st.write(f"Username: {username}")
        st.write(f"Email: {user['email']}")

        st.subheader("Preferences")
        preferences = user.get('preferences', {})
        new_preferences = {}
        for key, value in preferences.items():
            new_preferences[key] = st.text_input(f"{key}:", value=value)
        
        new_pref_key = st.text_input("Add new preference (key):")
        new_pref_value = st.text_input("Add new preference (value):")
        if new_pref_key and new_pref_value:
            new_preferences[new_pref_key] = new_pref_value

        if st.button("Update Preferences"):
            if user_manager.update_user_preferences(username, new_preferences):
                st.success("Preferences updated successfully!")
            else:
                st.error("Failed to update preferences.")

        if st.button("Delete Account"):
            if st.checkbox("Are you sure? This action cannot be undone."):
                # Implement account deletion logic here
                st.session_state.user = None
                st.success("Your account has been deleted.")
                st.experimental_rerun()
    else:
        st.warning("Please log in to view your profile.")