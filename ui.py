import streamlit as st
import time

def setup_ui(settings):
    with st.sidebar:
        st.image("./icons/brandlogo.png", width=50)
        st.sidebar.title(settings["sidebar"]["title"])
        st.sidebar.button(settings["sidebar"]["option1"])
        st.sidebar.button(settings["sidebar"]["option2"])
        st.sidebar.button(settings["sidebar"]["option3"])

def stream_data(text):
    for char in text:
        yield char
        time.sleep(0.015)

def display_greeting(settings):
    assistant_message_container = st.chat_message("assistant", avatar="./icons/assistant_image.png")
    message_placeholder = assistant_message_container.empty()

    partial_response = ""
    for chunk in stream_data(settings["greeting"]):
        partial_response += chunk
        message_placeholder.markdown(f"**{settings['bot_name']}**: {partial_response}")
    
    st.session_state['messages'].append({"role": "assistant", "content": f"**{settings['bot_name']}**: {settings['greeting']}"})

def display_chat_history(settings):
    for message in st.session_state.messages:
        if message["content"] == f"**{settings['bot_name']}**: {settings['greeting']}":
            continue  # Skip displaying the greeting message again
        with st.chat_message(message["role"], avatar=f"./icons/{str(message['role'])}_image.png"):
            st.markdown(message["content"])

