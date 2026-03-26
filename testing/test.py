import os
from groq import Groq
import sqlite3
import streamlit as st
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core import documents
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

#import .env  # Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv() 

# ... your existing imports (streamlit, groq, etc.)
#gobal variables and objects
conn = sqlite3.connect('company_knowledge_base.db')
cursor = conn.cursor()
#client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

# Create database
def create_database():
    conn = sqlite3.connect('company_knowledge_base.db')
    cursor = conn.cursor()

    # Create table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY,
        name TEXT,
        department TEXT,
        email TEXT,
        salary INTEGER,
        description TEXT
    )
    ''')

    conn.commit()
    conn.close()

    print('Database and table created successfully!')


def insert_sample_data():
    employees_data = [
        (1, 'Amit Sharma', 'Engineering', 'amit@company.com', 90000,
         'Backend engineer working on APIs and microservices.'),
        (2, 'Neha Verma', 'HR', 'neha@company.com', 60000,
         'Manages recruitment and employee engagement.'),
        (3, 'Rahul Mehta', 'Sales', 'rahul@company.com', 75000,
         'Handles enterprise sales and client acquisition.'),
        (4, 'Priya Singh', 'Engineering', 'priya@company.com', 95000,
         'Machine learning engineer working on AI models.'),
         (5, 'Rahul Thakare', 'Marketing', 'rahul@company.com', 70000, 'Manages marketing campaigns and brand strategy.')
    ]

    cursor.executemany('''
    INSERT OR REPLACE INTO employees
    VALUES (?, ?, ?, ?, ?, ?)
    ''', employees_data)

    conn.commit()
    conn.close()

    print('Sample data inserted successfully!')




# Load data from SQLite and convert to documents
def load_sqlite_data(db_path, table_name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]

    documents = []

    for row in rows:
        text = ' | '.join(
            f"{column_names[i]}: {row[i]}"
            for i in range(len(row))
        )

        documents.append(
            Document(
                page_content=text,
                metadata={'id': row[0]}
            )
        )

    conn.close()
    return documents


def create_vector_store(documents):
    embedding_model = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

    vector_store = Chroma.from_documents(
        documents,
        embedding_model,
        persist_directory=r'D:/Internship/chroma_db'   #'./chroma_db'
    )

    vector_store.persist()
    print('Embeddings stored in ChromaDB!')

    retriever = vector_store.as_retriever(search_kwargs={'k': 2})
    return retriever



def ask_groq(context, question):
    client = Groq(api_key=os.environ.get('GROQ_API_KEY'))
    prompt = f"""
    Use the following context to answer the question.

    Context:
    {context}

    Question:
    {question}
    """

    response = client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=[{'role': 'user', 'content': prompt}]
    )

    return response.choices[0].message.content




if __name__ == "__main__":
    create_database()
    insert_sample_data()

    documents = load_sqlite_data('company_knowledge_base.db', 'employees')
    retriever = create_vector_store(documents)

    # streamlit UI
    st.write('IT-Services Company Knowledge Base')
    question = st.text_input('Enter your question here')
    st.button('submit')

    #retriever = vector_store.as_retriever(search_kwargs={'k': 2})
    results = retriever.invoke(question)
    context = '\n'.join([doc.page_content for doc in results])

    answer = ask_groq(context, question)
    st.write(answer)
