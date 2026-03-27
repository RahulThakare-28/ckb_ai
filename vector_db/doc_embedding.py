"""
doc_embedding.py

Responsible for converting text documents into vector embeddings.

Design Principles:
- Loose coupling (no dependency on DB or vector store)
- Reusable embedding interface
- Robust error handling
- Clean and readable structure
"""

from typing import List, Union
from langchain_community.embeddings import HuggingFaceEmbeddings


class DocumentEmbedding:
    """
    Handles embedding generation for documents using HuggingFace models.

    Default Model:
        sentence-transformers/all-MiniLM-L6-v2
    """

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize embedding model.

        Args:
            model_name (str): HuggingFace embedding model name
        """
        try:
            self.model = HuggingFaceEmbeddings(model_name=model_name)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize embedding model: {e}")

    def embed_document(self, document: str) -> List[float]:
        """
        Generate embedding for a single document.

        Args:
            document (str): Input text

        Returns:
            List[float]: Embedding vector
        """
        if not isinstance(document, str):
            raise ValueError("Document must be a string")

        if not document.strip():
            raise ValueError("Document cannot be empty")

        try:
            return self.model.embed_query(document)
        except Exception as e:
            raise RuntimeError(f"Embedding failed for single document: {e}")

    def embed_documents(self, documents: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple documents.

        Args:
            documents (List[str]): List of text documents

        Returns:
            List[List[float]]: List of embedding vectors
        """
        if not isinstance(documents, list):
            raise ValueError("Documents must be a list of strings")

        if not documents:
            raise ValueError("Document list cannot be empty")

        for doc in documents:
            if not isinstance(doc, str) or not doc.strip():
                raise ValueError("Each document must be a non-empty string")

        try:
            return self.model.embed_documents(documents)
        except Exception as e:
            raise RuntimeError(f"Embedding failed for document list: {e}")

    def __call__(self, documents: Union[str, List[str]]) -> Union[List[float], List[List[float]]]:
        """
        Callable interface for flexibility.

        Args:
            documents (str or List[str])

        Returns:
            Embedding(s)
        """
        if isinstance(documents, str):
            return self.embed_document(documents)

        elif isinstance(documents, list):
            return self.embed_documents(documents)

        else:
            raise ValueError("Input must be a string or list of strings")