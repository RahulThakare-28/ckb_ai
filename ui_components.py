import streamlit as st
import base64

# =========================
# 🎨 LOAD CSS
# =========================
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# =========================
# 📊 SIDEBAR
# =========================
def render_sidebar():
    with st.sidebar:
        st.markdown("### System Status")

        st.success("Database: Connected")
        st.info("Vector Store: ChromaDB")
        st.warning("LLM: Groq")

        st.markdown("---")

        # Profile section at bottom
        st.markdown("""
        <div class="sidebar-profile">
            <img src="data:image/png;base64,{}" class="profile-img"/>
            <div class="profile-name">User</div>
        </div>
        """.format(get_base64("assets/user-logo.png")), unsafe_allow_html=True)

        st.button("Log Out", use_container_width=True)


# =========================
# 💬 CHAT RENDER
# =========================
def render_chat(messages):
    for msg in messages:
        if msg["role"] == "user":
            render_user_message(msg["content"])
        else:
            render_ai_message(msg["content"])


def render_user_message(text):
    st.markdown(f"""
    <div class="chat-row user">
        <div class="chat-bubble user-bubble">
            <div class="msg-text">{text}</div>
            <img src="data:image/png;base64,{get_base64("assets/user-logo.png")}" class="avatar"/>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_ai_message(text):
    st.markdown(f"""
    <div class="chat-row ai">
        <div class="chat-bubble ai-bubble">
            <img src="data:image/png;base64,{get_base64("assets/ai-logo.png")}" class="avatar"/>
            <div class="msg-text">{text}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# =========================
# 🔧 IMAGE HELPER
# =========================
def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()