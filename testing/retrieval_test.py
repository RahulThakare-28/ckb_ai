from vector_db.doc_embedding import DocumentEmbedding
from vector_db.vector_store import ChromaVectorStore
from vector_db.retrieval import Retriever

embedder = DocumentEmbedding()
vector_store = ChromaVectorStore()

retriever = Retriever(embedder, vector_store)

results = retriever.retrieve("Who is HR?", k=3)

for i, r in enumerate(results, 1):
    print(f"--- Result {i} ---")
    print(r["content"])
    print(r["metadata"])