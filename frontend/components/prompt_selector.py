import streamlit as st

def render(prompt_manager):
    st.subheader("Select a Prompt")

    prompt_options = ["Custom"] + [p.title for p in prompt_manager.get_popular_prompts(10)]
    selected_prompt = st.selectbox("Choose a prompt or enter your own:", prompt_options)

    if selected_prompt == "Custom":
        user_input = st.text_area("Enter your custom prompt:")
    else:
        prompt = prompt_manager.search_prompts(selected_prompt)[0]
        user_input = st.text_area("Your selected prompt:", value=prompt.content)
        prompt_manager.increment_prompt_usage(prompt.id)

    return user_input