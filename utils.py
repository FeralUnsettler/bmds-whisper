import whisper
import tempfile
import os
import base64
import streamlit as st

# -------------------------------
# Funções de transcrição
# -------------------------------
def transcribe_audio(audio_path, model_size="base"):
    """Transcreve o áudio usando Whisper OSS"""
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_path)
    return result["text"]

def save_to_md(text, filename=None):
    """Salva a transcrição em arquivo Markdown (.md)"""
    if filename is None:
        filename = f"transcricao.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("# Transcrição de Áudio\n\n")
        f.write(text)
    return filename

# -------------------------------
# Funções de cookies de sessão
# -------------------------------
def set_cookie(key, value):
    """Seta cookie na sessão do Streamlit"""
    st.session_state[key] = value

def get_cookie(key):
    """Lê cookie da sessão do Streamlit"""
    return st.session_state.get(key, None)

# -------------------------------
# Função de download customizado
# -------------------------------
def download_button(file_path, label):
    """Cria botão de download em Streamlit para arquivo local"""
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:file/markdown;base64,{b64}" download="{file_path}">{label}</a>'
    st.markdown(href, unsafe_allow_html=True)
