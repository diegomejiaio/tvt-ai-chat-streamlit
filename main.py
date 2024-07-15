import streamlit as st
from config import load_settings, load_api_key
from authentication import authenticate
from ui import setup_ui
from html_templates import css
import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
import time
import yaml

# Load settings and API key
# Load settings from the YAML file
with open("settings.yaml", "r") as file:
    settings = yaml.safe_load(file)

api_key = load_api_key()

# Set page configuration
st.set_page_config(page_title=settings["pagetitle"], page_icon="./icons/favicon.png")
st.write(css, unsafe_allow_html=True)

# Password verification
authenticate(settings)

# Set UI
setup_ui(settings)

# Funtion to stream text
def stream_data(text):
    for char in text:
        yield char
        time.sleep(0.015)

# Configuring the OpenAI API client
load_dotenv()
client = OpenAI(api_key=os.getenv("OPEN_API_KEY"))

# Extract settings for chat
instructions = settings["instructions"]
greeting = settings["greeting"]
placeholder = settings["placeholder"]
bot_name = settings["bot_name"]
person_name = settings["person_name"]
max_tokens = settings["max_tokens"]
temperature = settings["temperature"]

# Initialize OpenAI model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state['messages'] = []
# Display initial greeting in streaming
if "greeting_displayed" not in st.session_state:
    st.session_state["greeting_displayed"] = False

if not st.session_state["greeting_displayed"]:
    assistant_message_container = st.chat_message("assistant", avatar="./icons/assistant_image.png")
    message_placeholder = assistant_message_container.empty()

    partial_response = ""
    for chunk in stream_data(greeting):
        partial_response += chunk
        message_placeholder.markdown(f"**{bot_name}:** {partial_response}")
    
    st.session_state['messages'].append({"role": "assistant", "content": greeting})
    st.session_state["greeting_displayed"] = True
else:
    # Display chat messages from history
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        with st.chat_message(role, avatar=f"./icons/{role}_image.png"):
            if role == "assistant":
                st.markdown(f"**{bot_name}:** {content}")
            else:
                st.markdown(f"**{person_name}:** {content}")

# React to user input
if prompt := st.chat_input(placeholder=placeholder, max_chars=150):
    # Display user message in chat message container
    with st.chat_message("user", avatar="./icons/user_image.png"):
        st.markdown(f"**{person_name}:** {prompt}")
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Prepare the chat history for the API call
    messages = [
        {"role": "system", "content": instructions}
    ] + [
        {"role": message["role"], "content": message["content"]}
        for message in st.session_state.messages
    ]
    
    # Generate a response using OpenAI's API
    response = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        stop=None
    )
    # Extract the text from the response
    full_response = response.choices[0].message.content.strip()
    
    # Display assistant message in chat message container
    assistant_message_container = st.chat_message("assistant", avatar="./icons/assistant_image.png")
    message_placeholder = assistant_message_container.empty()

    partial_response = ""
    for chunk in stream_data(full_response):
        partial_response += chunk
        message_placeholder.markdown(f"**{bot_name}:** {partial_response}")

    # Add assistant message to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})