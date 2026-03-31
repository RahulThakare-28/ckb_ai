# Company Knowledge Base AI using RAG

---

## 📌 Project Overview

The **Company Knowledge Base AI** is an intelligent system developed to enhance how organizations access, manage, and utilize internal data. The project is based on **Retrieval-Augmented Generation (RAG)**, which combines semantic search with advanced Large Language Models (LLMs) to deliver accurate and context-aware responses.

Traditional systems rely on keyword-based search, which often fails to provide relevant results. This project overcomes that limitation by enabling users to interact with company data using **natural language queries** through an AI-powered chatbot interface.

The system retrieves relevant information from a knowledge base and generates human-like responses, making it easier for employees to access organizational knowledge efficiently.

---

## 🧠 Architecture Diagram

![Web Page](assets/chart-page.png)

---

## 🚀 Key Features

- Natural language-based query system  
- Semantic search using vector embeddings  
- Context-aware response generation  
- Fast inference using Groq LLM  
- Modular and scalable RAG architecture  
- Interactive chatbot UI using Streamlit  
- Integration with structured and unstructured data  

---

## 🧠 Technologies Used

- **LLM:** Groq  
- **Framework:** LangChain  
- **Vector Database:** ChromaDB  
- **Database:** MongoDB  
- **Embedding Model:** Hugging Face Transformers  
- **Frontend:** Streamlit  
- **Backend:** Python  

---

## ⚙️ System Workflow

The system follows a structured RAG pipeline:

1. User enters a query via the Streamlit interface  
2. Query is processed and converted into embeddings  
3. Embeddings are matched against stored vectors in ChromaDB  
4. Relevant documents are retrieved based on similarity  
5. Retrieved context is passed to the LLM (Groq) via LangChain  
6. LLM generates a natural language response  
7. Response is displayed to the user  

---

## 🏗️ Project Implementation Details

### 🔹 Data Layer

- MongoDB is used to store structured company data  
- Data includes employee records and organizational information  
- Acts as the primary source for building the knowledge base  

### 🔹 Embedding Generation

- Hugging Face transformer models are used  
- Converts text data into numerical vectors  
- Captures semantic meaning for better retrieval  

### 🔹 Vector Storage

- ChromaDB stores embeddings  
- Enables semantic similarity search  
- Improves retrieval accuracy over keyword search  

### 🔹 Retrieval Mechanism

- Retrieves top relevant documents  
- Based on vector similarity  
- Ensures context-aware information selection  

### 🔹 LLM Integration

- Groq is used for fast inference  
- Generates human-like responses  
- Integrated using LangChain pipeline  

### 🔹 Frontend Interface

- Built using Streamlit  
- Chatbot-style interaction  
- Displays responses dynamically  

---

## 🔐 Environment Variables

Create a `.env` file in the root directory and add:
