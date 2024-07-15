import streamlit as st
from openai import OpenAI
from ui import stream_data
from openai import OpenAI


def handle_user_input(settings, api_key):
    if prompt := st.chat_input(placeholder=settings["placeholder"], max_chars=150):
        with st.chat_message("user", avatar="./icons/user_image.png"):
            st.markdown(f"**{settings['person_name']}**: {prompt}")
        st.session_state.messages.append({"role": "user", "content": f"**{settings['person_name']}**: {prompt}"})
        
        messages = [
            {"role": message["role"], "content": message["content"].replace(f"**{settings['person_name']}**: ", "")}
            for message in st.session_state.messages
        ]
        messages.insert(0, {"role": "system", "content": settings["instructions"]})
        
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=messages,
        temperature=settings["temperature"],
        max_tokens=settings["max_tokens"],
        stop=None
    )
        full_response = response.choices[0].message.content.strip()

        assistant_message_container = st.chat_message("assistant", avatar="./icons/assistant_image.png")
        message_placeholder = assistant_message_container.empty()

        partial_response = ""
        for chunk in stream_data(full_response):
            partial_response += chunk
            message_placeholder.markdown(f"**{settings['bot_name']}**: {partial_response}")

        st.session_state.messages.append({"role": "assistant", "content": f"**{settings['bot_name']}**: {full_response}"})
