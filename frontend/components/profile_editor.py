import streamlit as st

def render(user, user_manager):
    st.subheader("Edit Profile")
    
    new_username = st.text_input("Username", user['username'])
    new_email = st.text_input("Email", user['email'])
    
    if st.button("Update Profile"):
        if user_manager.update_user(user['id'], new_username, new_email):
            st.success("Profile updated successfully!")
        else:
            st.error("Failed to update profile. Username or email might already be in use.")

    st.subheader("Change Password")
    current_password = st.text_input("Current Password", type="password")
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm New Password", type="password")

    if st.button("Change Password"):
        if new_password != confirm_password:
            st.error("New passwords do not match.")
        elif user_manager.change_password(user['id'], current_password, new_password):
            st.success("Password changed successfully!")
        else:
            st.error("Failed to change password. Please check your current password.")
