"""
app.py
Professional Conversational UI for IT-Services Knowledge Base
"""

import streamlit as st
import time
from main import build_vector_store, Retriever
from llm_models.groq_llm import get_llm_chain

# =========================
# ⚙️ BACKEND LAYER (LOGIC)
# =========================

@st.cache_resource
def load_system():
    vector_store, embedder = build_vector_store()
    retriever = Retriever(vector_store, embedder)
    chain = get_llm_chain()
    return retriever, chain

retriever, chain = load_system()


def query_engine(user_input: str):
    """
    Core logic isolated for debugging & reuse
    """
    try:
        # Step 1: Retrieve
        results = retriever.invoke(user_input)

        # Step 2: Build context
        context = "\n".join([
            str(doc["content"]) if isinstance(doc, dict)
            else str(doc.page_content)
            for doc in results
        ])

        # Step 3: LLM invoke
        response = chain.invoke({
            "context": context,
            "question": user_input
        })

        # Fix for your previous error
        if hasattr(response, "content"):
            return response.content
        elif isinstance(response, dict):
            return str(response)
        else:
            return str(response)

    except Exception as e:
        return f"Error: {str(e)}"


# =========================
# 🎨 UI CONFIG
# =========================

st.set_page_config(
    page_title="IT Services Knowledge Base",
    layout="wide"
)

# =========================
# 🎨 CUSTOM CSS (Professional Midnight Theme)
# =========================

st.markdown("""
<style>

/* Global */
.stApp {
    background-color: #0e1117;
    color: #e6edf3;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
}

/* Title */
h1, h2, h3 {
    color: #e6edf3;
}

/* Chat bubbles */
.user-bubble {
    border: 1px solid #00d4ff;
    padding: 12px;
    border-radius: 8px;
    background-color: transparent;
}

.assistant-bubble {
    background-color: #1a1f2b;
    padding: 12px;
    border-radius: 8px;
}

/* Chat input */
div[data-testid="stChatInput"] {
    border-top: 1px solid #00d4ff;
    padding-top: 10px;
}

textarea {
    border: 1px solid #00d4ff !important;
    border-radius: 6px !important;
}

textarea:focus {
    border: 1px solid #00d4ff !important;
    box-shadow: 0 0 8px #00d4ff !important;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 6px;
}
::-webkit-scrollbar-thumb {
    background: #00d4ff;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# =========================
# 📊 SIDEBAR (SYSTEM STATUS)
# =========================

st.sidebar.title("System Status")

st.sidebar.markdown("### Services")

st.sidebar.success("Database: Connected")
st.sidebar.info("Vector Store: ChromaDB")
st.sidebar.warning("LLM Provider: Groq")

st.sidebar.markdown("---")
st.sidebar.caption("IT Services Knowledge Base")


# =========================
# 💬 SESSION STATE
# =========================

if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================
# 🧠 HEADER
# =========================

st.title("IT-Services Knowledge Base")
st.caption("Query projects, employees, and internal company data")


# =========================
# 💬 CHAT HISTORY
# =========================

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):

        if msg["role"] == "user":
            st.markdown(
                f"<div class='user-bubble'>{msg['content']}</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div class='assistant-bubble'>{msg['content']}</div>",
                unsafe_allow_html=True
            )


# =========================
# ⌨️ CHAT INPUT
# =========================

user_input = st.chat_input("Ask about projects, employees, or clients...")

if user_input:

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Display user message
    with st.chat_message("user"):
        st.markdown(
            f"<div class='user-bubble'>{user_input}</div>",
            unsafe_allow_html=True
        )

    # Generate response
    with st.chat_message("assistant"):

        placeholder = st.empty()
        full_response = ""

        result = query_engine(user_input)

        # Typing effect
        for char in result:
            full_response += char
            placeholder.markdown(
                f"<div class='assistant-bubble'>{full_response}</div>",
                unsafe_allow_html=True
            )
            time.sleep(0.005)

    # Save assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": full_response
    })