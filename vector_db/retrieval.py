"""
retrieval.py
=========================
Responsible ONLY for retrieving relevant documents
from the vector store using similarity search.

Follows:
- Loose coupling
- Reusability
- Error handling
- Clean modular design
"""



class Retriever:
    """
    Retriever class to fetch top-k similar documents
    based on user query.

    This class:
    - Uses existing embedder
    - Uses existing vector store
    - Does NOT modify data
    """

    def __init__(self, embedder, vector_store):
        """
        :param embedder: Instance of DocumentEmbedding
        :param vector_store: Instance of ChromaVectorStore
        """
        self.embedder = embedder
        self.vector_store = vector_store

    def _validate_query(self, query):
        """Internal validation for query"""
        if not query or not isinstance(query, str):
            raise ValueError("Query must be a non-empty string")

    def retrieve(self, query, k=5):
        """
        Retrieve top-k similar documents.

        :param query: User query string
        :param k: Number of results
        :return: List of retrieved documents
        """
        try:
            # --------------------------
            # Step 1: Validate input
            # --------------------------
            self._validate_query(query)

            # --------------------------
            # Step 2: Generate embedding
            # --------------------------
            query_embedding = self.embedder.embed_document(query)

            if query_embedding is None:
                raise ValueError("Embedding generation failed for query")

            # --------------------------
            # Step 3: Similarity search
            # --------------------------
            results = self.vector_store.similarity_search(
                query_embedding,
                k=k
            )

            if results is None:
                raise ValueError("Vector store returned no results")

            # --------------------------
            # Step 4: Format results
            # --------------------------
            formatted_results = []

            for res in results:
                formatted_results.append({
                    "content": res.get("content"),
                    "metadata": res.get("metadata")
                })

            return formatted_results

        except Exception as e:
            print(f"❌ Retrieval Error: {e}")
            return []
        
 