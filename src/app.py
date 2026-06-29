import streamlit as st
import sqlite3
import datetime
import os
from database.vector_db import VectorDBManager
from rag.llm_factory import RAGPipeline

# 1. Configuración de Base de Datos para Logs
def init_log_db():
    conn = sqlite3.connect("data/logs.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS chat_logs
                      (id INTEGER PRIMARY KEY, timestamp TEXT, session_id TEXT, 
                       query TEXT, response TEXT)''')
    conn.commit()
    conn.close()

def log_interaction(session_id, query, response):
    conn = sqlite3.connect("data/logs.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat_logs (timestamp, session_id, query, response) VALUES (?, ?, ?, ?)",
                   (datetime.datetime.now().isoformat(), session_id, query, response))
    conn.commit()
    conn.close()

# 2. Inicialización de la App
st.set_page_config(page_title="DAVIbank Chatbot", page_icon="🤖")
st.title("🤖 Asistente Virtual DAVIbank")

# Inicializar componentes
if "db_manager" not in st.session_state:
    st.session_state.db_manager = VectorDBManager()
    st.session_state.rag = RAGPipeline(
        vector_store=st.session_state.db_manager.vector_store,
        llm_provider=os.getenv("LLM_PROVIDER", "groq")
    )
    init_log_db()

# 3. Historial del Chat en la UI
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Input del Usuario
if prompt := st.chat_input("¿En qué te puedo ayudar hoy?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Llamada al RAG
        response_data = st.session_state.rag.ask(prompt, session_id="user_session_1")
        response = response_data["answer"]
        st.markdown(response)
        
        # Loggear en SQLite
        log_interaction("user_session_1", prompt, response)

    st.session_state.messages.append({"role": "assistant", "content": response})