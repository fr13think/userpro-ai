import streamlit as st
from backend.conversation_engine import ConversationEngine
from backend.prompt_manager import PromptManager

def render(conversation_engine: ConversationEngine, prompt_manager: PromptManager):
    st.title("AI Conversation")

    if st.session_state.user:
        if 'messages' not in st.session_state:
            st.session_state.messages = []

        # Prompt selection
        st.subheader("Select a Prompt")
        prompt_options = ["Custom"] + [p.title for p in prompt_manager.get_popular_prompts(10)]
        selected_prompt = st.selectbox("Choose a prompt or enter your own:", prompt_options)

        if selected_prompt == "Custom":
            user_input = st.text_input("Your message:")
        else:
            prompt = prompt_manager.search_prompts(selected_prompt)[0]
            user_input = st.text_area("Your message:", value=prompt.content)
            prompt_manager.increment_prompt_usage(prompt.id)

        if st.button("Send"):
            response = conversation_engine.process_message(user_input)
            st.session_state.messages.append(f"You: {user_input}")
            st.session_state.messages.append(f"AI: {response}")
            st.experimental_rerun()

        for message in st.session_state.messages:
            st.text(message)

        if st.button("Start New Conversation"):
            st.session_state.messages = []
            conversation_engine.start_conversation()
            st.success("New conversation started!")

        if st.button("Save Conversation"):
            # Implement conversation saving logic here
            st.success("Conversation saved successfully!")

    else:
        st.warning("Please log in to start a conversation.")