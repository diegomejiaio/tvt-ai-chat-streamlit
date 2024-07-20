import streamlit as st
from authentication import authenticate
from ui import setup_ui
from html_templates import css
import os
from dotenv import load_dotenv
import time
import yaml
from openai import OpenAI
from vertexai import init
from vertexai.generative_models import GenerationConfig, GenerativeModel, HarmBlockThreshold, HarmCategory

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Establecer la variable de entorno para las credenciales de Google
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GCP_SA_KEY_PATH")

# Verificar que la variable de entorno se haya configurado correctamente
print("GOOGLE_APPLICATION_CREDENTIALS:", os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))

# Cargar las configuraciones desde el archivo YAML
with open("settings.yaml", "r", encoding='utf-8') as file:
    settings = yaml.safe_load(file)

# Cargar las claves de API desde las variables de entorno
openai_api_key = os.getenv("OPENAI_API_KEY")
project_id = os.getenv("GCP_PROJECT")
location = os.getenv("GCP_REGION")

# Configurar la página
st.set_page_config(page_title=settings["pagetitle"], page_icon="./icons/favicon.png")
st.write(css, unsafe_allow_html=True)

# Autenticación
authenticate(settings)

# Configurar la UI
setup_ui(settings)

# Función para stream de texto
def stream_data(text):
    for char in text:
        yield char
        time.sleep(0.015)

# Seleccionar el cliente de API basado en el proveedor
provider = st.session_state.get("provider", settings.get("provider", "openai"))
client = None

if provider == "openai":
    client = OpenAI(api_key=openai_api_key)
elif provider == "gemini":
    init(project=project_id, location=location)
    client = GenerativeModel("gemini-1.5-pro-001")  # Puedes ajustar el modelo según tus necesidades
else:
    st.error("Proveedor de IA no soportado")
    st.stop()

# Extraer configuraciones para el chat
instructions = settings["instructions"]
greeting = settings["greeting"]
placeholder = settings["placeholder"]
bot_name = settings["bot_name"]
person_name = settings["person_name"]
max_tokens = settings["max_tokens"]
temperature = settings["temperature"]

# Inicializar el modelo
if "model" not in st.session_state:
    st.session_state["model"] = "gpt-4-turbo" if provider == "openai" else "gemini-1.5-pro-001"

# Inicializar el historial del chat
if "messages" not in st.session_state:
    st.session_state['messages'] = []
# Mostrar el saludo inicial en streaming
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
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        with st.chat_message(role, avatar=f"./icons/{role}_image.png"):
            if role == "assistant":
                st.markdown(f"**{bot_name}:** {content}")
            else:
                st.markdown(f"**{person_name}:** {content}")

# Reaccionar al input del usuario
if prompt := st.chat_input(placeholder=placeholder, max_chars=150):
    with st.chat_message("user", avatar="./icons/user_image.png"):
        st.markdown(f"**{person_name}:** {prompt}")
    st.session_state.messages.append({"role": "user", "content": prompt})

    messages = [
        {"role": "system", "content": instructions}
    ] + [
        {"role": message["role"], "content": message["content"]}
        for message in st.session_state.messages
    ]

    if provider == "openai":
        response = client.chat.completions.create(
            model=st.session_state["model"],
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stop=None
        )
        full_response = response.choices[0].message.content.strip()
    elif provider == "gemini":
        # Construir el contenido adecuado para Gemini
        contents = "\n".join([message["content"] for message in messages])
        config = GenerationConfig(
            temperature=temperature, max_output_tokens=max_tokens
        )
        safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        }
        response = client.generate_content(
            contents=[contents],
            generation_config=config,
            safety_settings=safety_settings,
            stream=False
        )
        full_response = response.text.strip()

    assistant_message_container = st.chat_message("assistant", avatar="./icons/assistant_image.png")
    message_placeholder = assistant_message_container.empty()

    partial_response = ""
    for chunk in stream_data(full_response):
        partial_response += chunk
        message_placeholder.markdown(f"**{bot_name}:** {partial_response}")

    st.session_state.messages.append({"role": "assistant", "content": full_response})
