import streamlit as st

def render(conversation_engine, analytics_engine):
    st.subheader("Conversation")
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        st.text(message)

    user_input = st.text_input("Your message:")
    if st.button("Send"):
        response = conversation_engine.process_message(user_input)
        st.session_state.messages.append(f"You: {user_input}")
        st.session_state.messages.append(f"AI: {response}")

        # Log the conversation for analytics
        analytics_engine.log_conversation(
            st.session_state.user['id'], 
            len(st.session_state.messages),
            (datetime.now() - conversation_engine.start_time).total_seconds(),
            conversation_engine.get_conversation_topic()
        )

        st.experimental_rerun()

    if st.button("Start New Conversation"):
        st.session_state.messages = []
        conversation_engine.start_conversation()
        st.success("New conversation started!")