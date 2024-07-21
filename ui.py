import streamlit as st
import time

def setup_ui(settings):
    with st.sidebar:
        st.image("./icons/brandlogo.png", width=180)
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

        st.sidebar.markdown("---")  # Separador
        st.sidebar.markdown("© 2024 Todos los derechos reservados.")
        st.sidebar.markdown("Hecho con ❤️ por [Tivit](https://www.tivit.com/)")

# Función para stream de texto
def stream_data(text):
    for char in text:
        yield char
        time.sleep(0.009)

