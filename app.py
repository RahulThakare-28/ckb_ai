import streamlit as st
from main import build_vector_store, Retriever
from llm_models.groq_llm import get_llm_chain

@st.cache_resource
def load_system():
    vector_store, embedder = build_vector_store()
    retriever = Retriever(vector_store, embedder)
    chain = get_llm_chain()
    return retriever, chain

retriever, chain = load_system()

# ---------------- UI ----------------
st.markdown("""
    <style>
    .stTextInput input {
        background-color: #e3e7eefb !important;
        color: #00FF00 !important;
        border:  solid #FF4B4B !important;
    }
    </style>
    """, unsafe_allow_html=True
    )

st.set_page_config(page_title="IT-Services")
st.write('IT-Services Company Knowledge Base')

question = st.text_input('Ask a question...')
submit = st.button('Submit')

# ---------------- Logic ----------------

if submit and question.strip():  

    try:
        # Step 1: Retrieve
        results = retriever.invoke(question)

        # Step 2: Build context
        context = "\n".join([
            str(doc["content"]) if isinstance(doc, dict)
            else str(doc.page_content)
            for doc in results
        ])

        # Step 3: LLM invoke
        response = chain.invoke({
            "context": context,
            "question": question
        })

        answer = response.content if hasattr(response, "content") else str(response)

        st.write(answer)

    except Exception as e:
        st.error(f"❌ Error: {e}")


elif submit:
    st.warning("Please enter a question...!!!")
