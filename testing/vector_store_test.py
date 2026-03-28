"""
vector_store_test.py
=========================
End-to-end test for:
DB → Doc → Embedding → Vector Store → Similarity Search
"""

from httpcore import stream

from db_service.db_connections import MongoDBConnection

from vector_db.db_to_doc import (
    CollectionToDocumentConverter,
    DynamicDocumentTransformer
)

from vector_db.doc_embedding import DocumentEmbedding
from vector_db.vector_store import ChromaVectorStore
from vector_db.streams import fetch_data_stream

def run_test():
    try:
        print("✅ Connecting to MongoDB...")
        db = MongoDBConnection()
        database = db.get_database()

        collections = database.list_collection_names()
        print(f"📚 Collections: {collections}\n")

        # Init modules
        # converter = CollectionToDocumentConverter()
        # transformer = DynamicDocumentTransformer()
        transformer = DynamicDocumentTransformer()
        converter = CollectionToDocumentConverter(transformer)
        embedder = DocumentEmbedding()
        vector_store = ChromaVectorStore()

        # ==========================
        # STEP 1: Load & Convert Data
        # ==========================
        all_docs = []

        for collection_name in collections:
            print(f"📂 Processing collection: {collection_name}")
            collection = database[collection_name]

            # raw_docs = converter.convert_stream(collection)
            # transformed_docs = transformer.transform_record(raw_docs)
            #all_docs.extend(transformed_docs)
            # for raw_doc in converter.convert_stream(collection):
            #     transformed_doc = transformer.transform_record(raw_doc)
            #     all_docs.append(transformed_doc)
            # stream = fetch_data_stream(collection)
            # for raw_doc in converter.convert_stream(stream):
            #     transformed_doc = transformer.transform_record(raw_doc)
            #     all_docs.append(transformed_doc)
            stream = fetch_data_stream(collection)
            for doc in converter.convert_stream(stream):
                all_docs.append(doc)

        print(f"\n📝 Total documents: {len(all_docs)}")

        # ==========================
        # STEP 2: Generate Embeddings
        # ==========================
        print("\n⚙️ Generating embeddings...")
        #embeddings = embedder.embed_document(all_docs)
        texts = [doc.page_content for doc in all_docs]
        embeddings = embedder.embed_documents(texts)
        # Ensure alignment
        if len(all_docs) != len(embeddings):
            raise ValueError("Mismatch between documents and embeddings")

        # ==========================
        # STEP 3: Store in Vector DB
        # ==========================
        print("\n💾 Storing in vector store...")

        items = []
        for doc, emb in zip(all_docs, embeddings):
            items.append({
                "content": doc.page_content,
                "embedding": emb,
                "metadata": doc.metadata
            })

        ids = vector_store.bulk_add(items)
        print(f"✅ Stored {len(ids)} vectors")

        # ==========================
        # STEP 4: Query Test
        # ==========================
        print("\n🔍 Running similarity search test...")

        query = "Who is HR?"
        query_embedding = embedder.embed_document(query)

        results = vector_store.similarity_search(query_embedding, k=3)

        print(f"\n📌 Query: {query}\n")
        print("📊 Results:\n")

        for i, res in enumerate(results, 1):
            print(f"--- Result {i} ---")
            print(f"Content: {res['content']}")
            print(f"Metadata: {res['metadata']}\n")

        print("\n🎉 Vector Store Test Completed Successfully!")

    except Exception as e:
        print(f"❌ Test Failed: {e}")


if __name__ == "__main__":
    run_test()
