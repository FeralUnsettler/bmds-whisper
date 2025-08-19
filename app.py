import streamlit as st
from utils import transcribe_audio, save_to_md
import redis
import os
import tempfile
from streamlit_cookies_manager import EncryptedCookieManager

st.set_page_config(page_title="BMDS® Whisper ™", layout="wide")

# ==========================
# Sessão de cookies
# ==========================
cookies = EncryptedCookieManager(prefix="BMDS_Whisper", password="supersecretkey")
if not cookies.ready():
    st.stop()

# ==========================
# Cabeçalho do app
# ==========================
st.markdown(
    """
    <h1 style="text-align:center; font-size:3em; color:#2E86C1; font-weight:bold;">
        BMDS® Whisper ™
    </h1>
    """,
    unsafe_allow_html=True
)

# (Logotipo opcional, descomente depois que adicionar a imagem)
# st.image("static/logo.png", use_column_width=True)

st.write("Bem-vindo ao **BMDS® Whisper ™**. Faça upload de seu áudio para gerar uma transcrição automática em **Markdown (.md)**.")

# ==========================
# Sidebar
# ==========================
st.sidebar.header("Upload de Áudio e Progresso")
uploaded_file = st.sidebar.file_uploader("Escolha um arquivo de áudio", type=["mp3", "wav", "m4a"])

progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()

# ==========================
# Redis setup
# ==========================
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
r = redis.Redis.from_url(redis_url)

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name

    status_text.text("Processando o áudio com Whisper...")
    progress_bar.progress(30)

    # Transcrevendo
    result_text = transcribe_audio(tmp_file_path)

    progress_bar.progress(70)

    # Salvando em Redis temporário
    file_key = f"transcription:{cookies['session_id']}"
    r.setex(file_key, 3600, result_text)  # expira em 1h

    # Salvando arquivo markdown
    md_file = save_to_md(result_text)

    progress_bar.progress(100)
    status_text.text("Concluído ✅")

    # Download
    st.success("Transcrição concluída! Faça o download abaixo:")
    with open(md_file, "rb") as f:
        st.download_button("📥 Baixar Transcrição em Markdown", f, file_name="transcricao.md")
