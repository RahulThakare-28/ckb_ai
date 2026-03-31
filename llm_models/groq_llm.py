"""
groq_llm.py
=========================
LangChain-based Groq LLM wrapper using invoke()
"""

import os
from dotenv import load_dotenv
load_dotenv() 
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def get_llm_chain():
    """
    Returns a LangChain RunnableSequence using Groq
    """
    parser=StrOutputParser() 
    if not os.environ.get("GROQ_API_KEY"):
        raise ValueError(" GROQ_API_KEY not set")

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.1
    )

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are an intelligent assistant.

Use ONLY the provided context to answer the question.
If the answer is not present, say:
"I don't know, I not have any info about that."

Context:
{context}

Question:
{question}

Answer:
"""
    )

    # chain (this supports .invoke())
    chain = prompt | llm | parser

    return chain





