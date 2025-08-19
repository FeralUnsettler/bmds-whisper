import streamlit as st
import base64

# Cookies em Streamlit (via session_state + hack com JS)
def set_cookie(key, value):
    st.session_state[key] = value

def get_cookie(key):
    return st.session_state.get(key, None)

# Botão de download customizado
def download_button(file_path, label):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:file/markdown;base64,{b64}" download="{file_path}">{label}</a>'
    st.markdown(href, unsafe_allow_html=True)
