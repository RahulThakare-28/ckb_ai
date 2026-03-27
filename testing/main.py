import streamlit as st
from agent_setup import get_llm_agent
from langgraph.types import Command

import os
from dotenv import load_dotenv
load_dotenv() 

# Page Config for centering
st.set_page_config(layout="wide")

def initialize_session():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = "user_conversation_1"

def display_chat():
    # CSS for WhatsApp-like UI with centered columns
    st.markdown("""
        <style>
        .chat-container { display: flex; flex-direction: column; }
        .user-msg { align-self: flex-end; background-color: #dcf8c6; padding: 10px; border-radius: 10px; margin: 5px; max-width: 70%; }
        .bot-msg { align-self: flex-start; background-color: #f0f0f0; padding: 10px; border-radius: 10px; margin: 5px; max-width: 70%; }
        </style>
    """)

    # Creating equal margins (Left Margin | Center Chat | Right Margin)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f'<div class="user-msg">{msg["content"]}</div>')
            else:
                st.markdown(f'<div class="bot-msg">{msg["content"]}</div>')

def handle_input(agent):
    # Bottom input box
    prompt = st.chat_input("Type your message here...")
    
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        config = {"configurable": {"thread_id": st.session_state.thread_id}}
        
        # Invoke agent
        result = agent.invoke(
            {"messages": [{"role": "user", "content": prompt}]}, 
            config=config, 
            version="v2"
        )

        # Check for Clarification Interrupt
        if result.interrupts:
            # If the model is confused, it triggers an interrupt
            clarification_text = "I'm not sure what you mean. Could you clarify?"
            st.session_state.messages.append({"role": "assistant", "content": clarification_text})
        else:
            # Normal response
            response = result.value["messages"][-1].content
            st.session_state.messages.append({"role": "assistant", "content": response})
        
        st.rerun()

def main():
    st.title("Groq Agent with Human-in-the-Loop")
    
    api_key = os.environ.get('GROQ_API_KEY') # Secure this in st.secrets
    agent = get_llm_agent(api_key)
    
    initialize_session()
    display_chat()
    handle_input(agent)

if __name__ == "__main__":
    main()