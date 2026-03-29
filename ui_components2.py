import streamlit as st
import base64
import os

# =========================
# CSS
# =========================
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# =========================
# SIDEBAR
# =========================
# def render_sidebar():
#     with st.sidebar:

#         # Company logo (top-right)
#         st.markdown(f"""
#         <div class="sidebar-header">
#             <img src="data:image/png;base64,{get_base64("assets/company-logo.png")}" class="company-logo"/>
#         </div>
#         """, unsafe_allow_html=True)

#         st.markdown("### System Status")

#         st.success("Database: Connected")
#         st.info("Vector Store: ChromaDB")
#         st.warning("LLM: Groq")

#         st.markdown("---")

#         # Profile bottom
#         st.markdown(f"""
#         <div class="sidebar-profile">
#             <img src="data:image/png;base64,{get_base64("assets/user-logo.png")}" class="profile-img"/>
#             <div class="profile-name">User</div>
#         </div>
#         """, unsafe_allow_html=True)

#         st.button("Log Out", use_container_width=True)
def render_sidebar():
    with st.sidebar:

        # =========================
        # 🔝 COMPANY LOGO (TOP)
        # =========================
        st.markdown(f"""
        <div class="sidebar-header">
            <img src="data:image/png;base64,{get_base64("assets/company-logo.png")}" />
        </div>
        """, unsafe_allow_html=True)

        # =========================
        # 📊 SYSTEM STATUS
        # =========================
        st.markdown("### System Status")

        st.success("Database: Connected")
        st.info("Vector Store: ChromaDB")
        st.warning("LLM: Groq")

        st.markdown("---")

        # =========================
        # 👤 PROFILE (BOTTOM)
        # =========================
        st.markdown(f"""
        <div class="sidebar-profile">
            <img src="data:image/png;base64,{get_base64("assets/user-logo.png")}" />
            <div class="profile-name">User</div>
        </div>
        """, unsafe_allow_html=True)

        st.button("Log Out", use_container_width=True)

# =========================
# CHAT RENDER
# =========================
def render_chat(messages):
    for msg in messages:
        if msg["role"] == "user":
            render_user_message(msg["content"])
        else:
            render_ai_message(msg["content"])


def render_user_message(text):
    st.markdown(f"""
    <div class="chat-wrapper user">
        <div class="avatar-container user">
            <img src="data:image/png;base64,{get_base64("assets/user-logo.png")}" />
        </div>
        <div class="chat-bubble user-bubble">
            {text}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_ai_message(text):
    st.markdown(f"""
    <div class="chat-wrapper ai">
        <div class="avatar-container ai">
            <img src="data:image/png;base64,{get_base64("assets/ai-logo.png")}" />
        </div>
        <div class="chat-bubble ai-bubble">
            {text}
        </div>
    </div>
    """, unsafe_allow_html=True)


# =========================
# IMAGE HELPER (SAFE PATH)
# =========================
def get_base64(file_path):
    base_dir = os.path.dirname(__file__)
    full_path = os.path.join(base_dir, file_path)

    with open(full_path, "rb") as f:
        return base64.b64encode(f.read()).decode()