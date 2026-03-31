import streamlit as st
import time
from main import build_vector_store, Retriever
from llm_models.groq_llm import get_llm_chain

from ui_components import load_css, render_sidebar, render_chat


# =========================
# BACKEND 
# =========================
@st.cache_resource
def load_system():
    vector_store, embedder = build_vector_store()
    retriever = Retriever(vector_store, embedder)
    chain = get_llm_chain()
    return retriever, chain

retriever, chain = load_system()


def query_engine(user_input: str):
    try:
        results = retriever.invoke(user_input)

        context = "\n".join([
            str(doc["content"]) if isinstance(doc, dict)
            else str(doc.page_content)
            for doc in results
        ])

        response = chain.invoke({
            "context": context,
            "question": user_input
        })

        if hasattr(response, "content"):
            return response.content
        return str(response)

    except Exception as e:
        return f"Error: {str(e)}"


# =========================
# UI CONFIG
# =========================


st.set_page_config(layout="wide", page_icon="assets/ai-logo.png", page_title="CKB AI")

load_css("style.css")
render_sidebar()

# =========================
# SESSION STATE
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# CHAT
# =========================
render_chat(st.session_state.messages)

# =========================
# INPUT
# =========================
user_input = st.chat_input("Ask about projects, employees, or clients...")

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        result = query_engine(user_input)

        for char in result:
            full_response += char
            placeholder.markdown(full_response)
            time.sleep(0.003)

    st.session_state.messages.append({
        "role": "assistant",
        "content": full_response
    })

    st.rerun()