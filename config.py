import streamlit as st
from ui import setup_ui
import yaml

# Cargar las configuraciones desde el archivo YAML
with open("settings.yaml", "r", encoding='utf-8') as file:
    settings = yaml.safe_load(file)

def show_settings_page():
    st.title("Configuraciones")
    setup_ui(settings)

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

show_settings_page()
