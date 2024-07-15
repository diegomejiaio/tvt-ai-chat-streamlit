import streamlit as st

def authenticate(settings):
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

    if not st.session_state["password_correct"] and not settings["disablePassword"]:
        st.title("Autenticación requerida")
        st.text_input("Introduce la contraseña", type="password", on_change=check_password, key="password")
        st.stop()
