"""
main.py
=========================
Entry point using LangChain invoke()
"""


from db_service.db_connections import MongoDBConnection

from vector_db.db_to_doc import (
    CollectionToDocumentConverter,
    DynamicDocumentTransformer
)

from vector_db.doc_embedding import DocumentEmbedding
from vector_db.vector_store import ChromaVectorStore
from vector_db.streams import fetch_data_stream


from llm_models.groq_llm import get_llm_chain


def build_vector_store():
    db = MongoDBConnection()
    database = db.get_database()

    transformer = DynamicDocumentTransformer()
    converter = CollectionToDocumentConverter(transformer)
    embedder = DocumentEmbedding()
    vector_store = ChromaVectorStore()

    all_docs = []

    for collection_name in database.list_collection_names():
        collection = database[collection_name]
        stream = fetch_data_stream(collection)

        for doc in converter.convert_stream(stream):
            all_docs.append(doc)

    print(f"📝 Loaded {len(all_docs)} documents")

    texts = [doc.page_content for doc in all_docs]
    embeddings = embedder.embed_documents(texts)

    items = []
    for doc, emb in zip(all_docs, embeddings):
        items.append({
            "content": doc.page_content,
            "embedding": emb,
            "metadata": doc.metadata
        })

    vector_store.bulk_add(items)

    return vector_store, embedder


# ✅ LangChain-style retriever wrapper
class Retriever:
    def __init__(self, vector_store, embedder):
        self.vector_store = vector_store
        self.embedder = embedder

    def invoke(self, query: str):
        query_embedding = self.embedder.embed_document(query)
        return self.vector_store.similarity_search(query_embedding, k=3)


def main():
    try:
        print("🚀 Starting system...\n")

        vector_store, embedder = build_vector_store()

        retriever = Retriever(vector_store, embedder)

        # chain
        chain = get_llm_chain()

        while True:
            question = input("\n💬 Ask a question (or type 'exit'): ")

            if question.lower() == "exit":
                break

            # Step 1: Retrieve
            results = retriever.invoke(question)

            # Step 2: Build context
            context = "\n".join([
                str(doc["content"]) if isinstance(doc, dict)
                else str(doc.page_content)
                for doc in results
            ])

            # Step 3: LLM invoke (REAL LangChain invoke)
            response = chain.invoke({
                "context": context,
                "question": question
            })

            #print("\n🤖 Answer:\n", response.content)
            # Safe handling
            answer = response.content if hasattr(response, "content") else str(response)

            print("\n🤖 Answer:\n", answer)

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()



'''
o/p :
🚀 Starting system...
📝 Loaded 8 documents

💬 Ask a question (or type 'exit'): tell me name of HR

🤖 Answer:
 Neha Verma

💬 Ask a question (or type 'exit'): give me all details , you know about th
e neha verma

🤖 Answer:
 Based on the given data, here are the details about Neha Verma:

- _id: 2
- name: Neha Verma
- department: HR
- email: neha@company.com
- salary: 60000
- description: Manages recruitment and employee engagement.

💬 Ask a question (or type 'exit'): exit
'''