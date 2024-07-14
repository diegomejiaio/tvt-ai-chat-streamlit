import streamlit as st
from openai import OpenAI
from html_templates import css
import os
from dotenv import load_dotenv
import time
import yaml

# Load settings from the YAML file
with open("settings.yaml", "r") as file:
    settings = yaml.safe_load(file)

# Set page title and favicon
st.set_page_config(page_title=settings["pagetitle"], page_icon="./icons/favicon.png")
st.write(css, unsafe_allow_html=True)

# Configuring the OpenAI API client
load_dotenv()
client = OpenAI(api_key=os.getenv("OPEN_API_KEY"))

# Password verification
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False
if "password_attempts" not in st.session_state:
    st.session_state["password_attempts"] = 0

def check_password():
    if st.session_state["password"] == settings["password"]:
        st.session_state["password_correct"] = True
    else:
        st.session_state["password_attempts"] += 1
        st.error("Contraseña incorrecta")
        if st.session_state["password_attempts"] >= 2:
            st.stop()

if not st.session_state["password_correct"]:
    st.title("Autenticación requerida")
    st.text_input("Introduce la contraseña", type="password", on_change=check_password, key="password")
    st.stop()

# Set UI
with st.sidebar:
    st.image("./icons/brandlogo.png", width=50)
    st.sidebar.title(settings["sidebar"]["title"])
    st.sidebar.button(settings["sidebar"]["option1"])
    st.sidebar.button(settings["sidebar"]["option2"])
    st.sidebar.button(settings["sidebar"]["option3"])

def stream_data(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.12)

# Extract settings for chat
instructions = settings["instructions"]
greeting = settings["greeting"]
placeholder = settings["placeholder"]
bot_name = settings["bot_name"]
person_name = settings["person_name"]

# Initialize OpenAI model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

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
    
    st.session_state['messages'].append({"role": "assistant", "content": f"**{bot_name}:** {greeting}"})
    st.session_state["greeting_displayed"] = True
else:
    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=f"./icons/{str(message['role'])}_image.png"):
            st.markdown(message["content"])

# React to user input
if prompt := st.chat_input(placeholder=placeholder, max_chars=150):
    # Display user message in chat message container
    with st.chat_message("user", avatar="./icons/user_image.png"):
        st.markdown(f"**{person_name}:** {prompt}")
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": f"**{person_name}:** {prompt}"})
    # Prepare the chat history for the API call
    messages = [
        {"role": message["role"], "content": message["content"].replace(f"**{person_name}:** ", "")}
        for message in st.session_state.messages
    ]
    messages.insert(0, {"role": "system", "content": instructions})
    
    # Generate a response using OpenAI's API
    response = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=messages,
        temperature=settings["temperature"],
        max_tokens=150,
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
    st.session_state.messages.append({"role": "assistant", "content": f"**{bot_name}:** {full_response}"})
