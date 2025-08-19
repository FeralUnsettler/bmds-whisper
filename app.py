import streamlit as st
import redis
import os
import tempfile
from utils import transcribe_audio, save_to_md, set_cookie, get_cookie, download_button

# -------------------------------
# Configuração página
# -------------------------------
st.set_page_config(page_title="BMDS® Whisper ™", layout="wide")

# -------------------------------
# Sessão via cookie
# -------------------------------
session_id = get_cookie("session_id")
if not session_id:
    import uuid
    session_id = str(uuid.uuid4())
    set_cookie("session_id", session_id)

# -------------------------------
# Redis Config via env ou defaults
# -------------------------------
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
r = redis.Redis.from_url(REDIS_URL)

# -------------------------------
# Header do app
# -------------------------------
st.markdown(
    "<h1 style='text-align:center; font-size:3rem; color:#1E90FF; font-weight:bold;'>BMDS® Whisper ™</h1>",
    unsafe_allow_html=True
)
# st.image("assets/logo.png", use_column_width=True)  # Logo comentado

st.write("Faça upload de um arquivo de áudio para gerar a transcrição em Markdown (.md)")

# -------------------------------
# Sidebar
# -------------------------------
st.sidebar.header("Upload e Progresso")
uploaded_file = st.sidebar.file_uploader("Escolha um áudio:", type=["mp3", "wav", "m4a"])

progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()

# -------------------------------
# Processamento
# -------------------------------
if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name

    status_text.text("⏳ Transcrevendo áudio com Whisper...")
    progress_bar.progress(30)

    transcript = transcribe_audio(tmp_path)

    progress_bar.progress(70)

    # Salvar temporariamente no Redis (1h)
    r.setex(f"transcription:{session_id}", 3600, transcript)

    md_file = save_to_md(transcript)

    progress_bar.progress(100)
    status_text.text("✅ Transcrição concluída!")

    st.success("Transcrição pronta! Faça o download:")
    download_button(md_file, "📥 Baixar Transcrição (.MD)")st.sidebar.header("Upload de Áudio e Progresso")
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
