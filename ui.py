import streamlit as st
import time
import yaml

def setup_ui(settings):
    with st.sidebar:
        st.image("./icons/brandlogo.png", width=250)
        st.sidebar.title(settings["sidebar"]["title"])
        st.sidebar.button(settings["sidebar"]["option1"])
        st.sidebar.button(settings["sidebar"]["option2"])
        st.sidebar.button(settings["sidebar"]["option3"])
        st.sidebar.markdown("---")  # Separador
        provider = st.sidebar.selectbox(
            "Seleccione el proveedor de IA",
            ("openai", "gemini"),
            index=["openai", "gemini"].index(settings.get("provider", "openai"))
        )
        st.session_state["provider"] = provider

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

def show_settings_page(settings):
    st.title("Configuraciones")

    # Editable settings
    instructions = st.text_area("Instructions", value=settings.get("instructions", ""))
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=settings.get("temperature", 0.7), step=0.01)
    provider = st.selectbox("Provider", options=["openai", "gemini"], index=["openai", "gemini"].index(settings.get("provider", "openai")))

    if st.button("Guardar Configuraciones"):
        settings["instructions"] = instructions
        settings["temperature"] = temperature
        settings["provider"] = provider
        with open("settings.yaml", "w", encoding='utf-8') as file:
            yaml.dump(settings, file, allow_unicode=True)
        st.success("Configuraciones guardadas con éxito.")
