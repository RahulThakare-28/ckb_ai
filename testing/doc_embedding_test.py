
"""
db_embedding_test.py

Integration test for DocumentEmbedding module using real MongoDB data.

Flow:
    MongoDB → dynamic collection discovery
             → fetch_data_stream
             → db_to_doc conversion
             → DocumentEmbedding
"""

from typing import List

from db_service.db_connections import MongoDBConnection

from vector_db.db_to_doc import (
    CollectionToDocumentConverter,
    DynamicDocumentTransformer
)

from vector_db.doc_embedding import DocumentEmbedding


class DBEmbeddingTest:
    """
    End-to-end test for document embedding pipeline.
    """

    def __init__(self, sample_limit: int = 5):
        self.sample_limit = sample_limit
        self.documents: List[str] = []

    def setup(self):
        """
        Setup DB connection and fetch documents correctly.
        """
        try:
            # Step 1: Connect to DB
            connection = MongoDBConnection()
            db = connection.get_database()

            if db is None:
                raise RuntimeError("Database connection failed")

            # Step 2: Get collections dynamically
            collections = db.list_collection_names()

            if not collections:
                raise RuntimeError("No collections found in database")

            # Step 3: Initialize converter pipeline
            transformer = DynamicDocumentTransformer()
            converter = CollectionToDocumentConverter(transformer)

            # Step 4: Process each collection
            for collection_name in collections:
                try:
                    collection = db[collection_name]

                    # ✅ Fetch limited records properly
                    records = list(collection.find().limit(self.sample_limit))

                    # ✅ Convert in batch (CORRECT usage)
                    docs = converter.convert(records)

                    # ✅ Extract page_content
                    for d in docs:
                        if d.page_content.strip():
                            self.documents.append(d.page_content)

                except Exception as e:
                    print(f"[WARN] Skipping collection '{collection_name}': {e}")

            if not self.documents:
                raise RuntimeError("No valid documents generated from DB")

        except Exception as e:
            raise RuntimeError(f"Setup failed: {e}")

    def test_single_embedding(self, embedder: DocumentEmbedding):
        """
        Test embedding for a single document.
        """
        print("\n--- Single Embedding Test ---")

        try:
            doc = self.documents[0]
            vector = embedder.embed_document(doc)

            print(f"Doc preview: {doc[:80]}...")
            print(f"Vector dimension: {len(vector)}")

            assert isinstance(vector, list), "Embedding must be list"
            assert len(vector) > 0, "Embedding cannot be empty"

        except Exception as e:
            raise RuntimeError(f"Single embedding test failed: {e}")

    def test_batch_embedding(self, embedder: DocumentEmbedding):
        """
        Test embedding for multiple documents.
        """
        print("\n--- Batch Embedding Test ---")

        try:
            vectors = embedder.embed_documents(self.documents)

            print(f"Documents: {len(self.documents)}")
            print(f"Embeddings: {len(vectors)}")

            assert len(vectors) == len(self.documents), "Count mismatch"

            for vec in vectors:
                assert isinstance(vec, list), "Each embedding must be list"
                assert len(vec) > 0, "Embedding cannot be empty"

        except Exception as e:
            raise RuntimeError(f"Batch embedding test failed: {e}")

    def run(self):
        """
        Run full test pipeline.
        """
        print("🚀 Starting DB Embedding Integration Test")

        try:
            self.setup()
            print(f"✅ Loaded {len(self.documents)} documents")

            embedder = DocumentEmbedding()
            print("✅ Embedding model initialized")

            self.test_single_embedding(embedder)
            self.test_batch_embedding(embedder)

            print("\n🎉 All tests passed successfully!")

        except Exception as e:
            print(f"\n❌ Test failed: {e}")


if __name__ == "__main__":
    test = DBEmbeddingTest(sample_limit=5)
    test.run()

