import streamlit as st
from backend.prompt_manager import PromptManager

def render(prompt_manager: PromptManager):
    st.title("Prompt Management")

    if st.session_state.user:
        user_id = st.session_state.user['id']

        # Create new prompt
        st.header("Create New Prompt")
        new_prompt_title = st.text_input("Prompt Title")
        new_prompt_content = st.text_area("Prompt Content")
        new_prompt_tags = st.text_input("Tags (comma-separated)")
        if st.button("Create Prompt"):
            tags = [tag.strip() for tag in new_prompt_tags.split(',')] if new_prompt_tags else []
            prompt = prompt_manager.create_prompt(new_prompt_title, new_prompt_content, user_id, tags)
            st.success(f"Created new prompt: {prompt.title}")

        # List user's prompts
        st.header("Your Prompts")
        user_prompts = prompt_manager.get_user_prompts(user_id)
        for prompt in user_prompts:
            with st.expander(prompt.title):
                st.write(prompt.content)
                st.write(f"Tags: {', '.join(prompt.tags)}")
                st.write(f"Usage count: {prompt.usage_count}")
                if st.button(f"Delete {prompt.title}"):
                    if prompt_manager.delete_prompt(prompt.id):
                        st.success(f"Deleted prompt: {prompt.title}")
                        st.experimental_rerun()

        # Search prompts
        st.header("Search Prompts")
        search_query = st.text_input("Search for prompts")
        if search_query:
            search_results = prompt_manager.search_prompts(search_query)
            for prompt in search_results:
                st.write(f"{prompt.title} (by User {prompt.user_id})")

        # Popular prompts
        st.header("Popular Prompts")
        popular_prompts = prompt_manager.get_popular_prompts(5)
        for prompt in popular_prompts:
            st.write(f"{prompt.title} (Used {prompt.usage_count} times)")

        # Prompt statistics
        st.header("Prompt Statistics")
        stats = prompt_manager.get_prompt_statistics()
        st.write(f"Total Prompts: {stats['total_prompts']}")
        st.write(f"Average Usage: {stats['average_usage']:.2f}")
        st.write(f"Most Used Prompt: {stats['most_used_prompt']}")

    else:
        st.warning("Please log in to manage prompts.")