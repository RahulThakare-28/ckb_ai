"""
vector_store.py
----------------
Responsibility:
- Accept embeddings from doc_embedding.py
- Store vectors in ChromaDB
- Avoid recomputation (id-based caching)
- Provide retriever interface for LLM layer

Design Principles:
- Loose coupling (NO embedding generation here)
- Clear separation of concerns
- Error handling at each layer
- Production-ready (ChromaDB)
"""

import hashlib
from typing import List, Dict, Any, Optional

#from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma
from langchain_core.documents import Document


class VectorStoreError(Exception):
    """Custom exception for vector store errors"""
    pass


class ChromaVectorStore:
    """
    ChromaDB-based vector store.

    IMPORTANT:
    - Does NOT generate embeddings
    - Accepts embeddings from doc_embedding.py
    - Ensures idempotent storage
    """

    def __init__(
        self,
        persist_directory: str = "D:/chroma_db",
        collection_name: str = "default_collection"
    ):
        try:
            self._store = Chroma(
                collection_name=collection_name,
                persist_directory=persist_directory
            )

        except Exception as e:
            raise VectorStoreError(f"Failed to initialize Chroma store: {e}")

    # ==========================
    # Internal Helpers
    # ==========================

    def _generate_id(self, content: str) -> str:
        try:
            return hashlib.sha256(content.encode("utf-8")).hexdigest()
        except Exception as e:
            raise VectorStoreError(f"Failed to generate ID: {e}")

    # ==========================
    # Public APIs
    # ==========================

    # def add(
    #     self,
    #     content: str,
    #     embedding: List[float],
    #     metadata: Optional[Dict[str, Any]] = None
    # ) -> str:
    #     """
    #     Add embedding to Chroma (idempotent)
    #     """
    #     try:
    #         doc_id = self._generate_id(content)

    #         # Check if exists
    #         #existing = self._store._collection.get(ids=[doc_id])
    #         #if existing and existing.get("ids"):
    #         existing = self._store.get(ids=[doc_id])
    #         if existing is not None and len(existing.get("ids", [])) > 0:
    #             return doc_id

    #         self._store.add_documents(
    #             ids=[doc_id],
    #             embeddings=[embedding],
    #             documents=[content],
    #             metadatas=[metadata or {}]
    #         )

    #         self._store.persist()
    #         return doc_id

    #     except Exception as e:
    #         raise VectorStoreError(f"Failed to add vector: {e}")
    def add(self, content: str, embedding: List[float],     metadata: Optional[Dict[str, Any]] = None) -> str:
        try:
            doc_id = self._generate_id(content)

            existing = self._store.get(ids=[doc_id])
            if existing is not None and len(existing.get("ids", [])) > 0:
                return doc_id

            doc = Document(page_content=content, metadata=metadata or {})

            self._store.add_documents(
                documents=[doc],
                ids=[doc_id], #IMPORTANT
                #embeddings=[embedding]
                )

            self._store
            return doc_id

        except Exception as e:
            raise VectorStoreError(f"Failed to add vector: {e}")

    # def bulk_add(self, items: List[Dict[str, Any]]) -> List[str]:
    #     """
    #     Bulk insert
    #     items = [
    #         {
    #             "content": str,
    #             "embedding": [...],
    #             "metadata": {...}
    #         }
    #     ]
    #     """
    #     try:
    #         ids = []
    #         embeddings = []
    #         documents = []
    #         metadatas = []

    #         for item in items:
    #             content = item["content"]
    #             doc_id = self._generate_id(content)

    #             ids.append(doc_id)
    #             embeddings.append(item["embedding"])
    #             documents.append(content)
    #             metadatas.append(item.get("metadata", {}))

    #         self._store.add_documents(
    #             ids=ids,
    #             embeddings=embeddings,
    #             documents=documents,
    #             metadatas=metadatas
    #         )

    #         self._store.persist()
    #         return ids

    #     except Exception as e:
    #         raise VectorStoreError(f"Bulk insert failed: {e}")

    def bulk_add(self, items: List[Dict[str, Any]]) -> List[str]:
        try:
            docs = []
            ids = []

            for item in items:
                content = item["content"]
                doc_id = self._generate_id(content)
               
                #check BEFORE inserting is already exists
                existing = self._store.get(ids=[doc_id])
                if existing and existing.get("ids"):
                    continue
                ids.append(doc_id)

                docs.append(
                    Document(
                        page_content=content,
                        metadata=item.get("metadata", {})
                    )
                )

            #self._store.add_documents(docs)
            if docs:
                self._store.add_documents(
                documents=docs,
                ids=ids   #  CRITICAL FIX
            )

            #self._store
            return ids

        except Exception as e:
            raise VectorStoreError(f"Bulk insert failed: {e}")






    def similarity_search(
        self,
        query_embedding: List[float],
        k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Perform similarity search using embedding (NOT raw query)
        """
        try:
            # results = self._store.query(
            #     query_embeddings=[query_embedding],
            #     n_results=k
            results = self._store.similarity_search_by_vector(
                embedding=query_embedding,
                k=k
            )

            # output = []
            # for i in range(len(results.get("ids", [])[0])):
            #     output.append({
            #         "id": results["ids"][0][i],
            #         "content": results["documents"][0][i],
            #         "metadata": results["metadatas"][0][i]
            #     })

            # return output
            output = []
            for doc in results:
                output.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata
                })

            return output

        except Exception as e:
            raise VectorStoreError(f"Similarity search failed: {e}")

    def get(self, doc_id: str) -> Optional[Dict[str, Any]]:
        try:
            result = self._store.get(ids=[doc_id])
            if result and result.get("documents"):
                return {
                    "content": result["documents"][0],
                    "metadata": result["metadatas"][0]
                }
            #return None
            return result is not None and len(result.get("ids", [])) > 0
        except Exception as e:
            raise VectorStoreError(f"Get failed: {e}")

    def delete(self, doc_id: str) -> bool:
        try:
            self._store.delete(ids=[doc_id])
            self._store
            return True
        except Exception as e:
            raise VectorStoreError(f"Delete failed: {e}")

    def exists(self, content: str) -> bool:
        try:
            doc_id = self._generate_id(content)
            result = self._store.get(ids=[doc_id])
            return bool(result and result.get("ids"))
        except Exception as e:
            raise VectorStoreError(f"Exist check failed: {e}")


# ==========================
# Future Interface
# ==========================

class BaseVectorStore:
    def add(self, content: str, embedding: List[float], metadata: Dict[str, Any]):
        raise NotImplementedError

    def bulk_add(self, items: List[Dict[str, Any]]):
        raise NotImplementedError

    def similarity_search(self, query_embedding: List[float], k: int = 5):
        raise NotImplementedError

    def get(self, doc_id: str):
        raise NotImplementedError

    def delete(self, doc_id: str):
        raise NotImplementedError

    def exists(self, content: str):
        raise NotImplementedError
