"""
Module: db_to_doc.py

Purpose:
    Convert database records into LangChain Document objects.

Features:
    - Supports structured & dynamic schema
    - Streaming support for large datasets
    - Layered error handling for debugging
    - Clean, modular, reusable design
"""

from typing import List, Dict, Any, Callable, Optional, Iterable
from langchain_core.documents import Document



# Base Transformer
class DocumentTransformer:
    """
    Transforms structured records into LangChain Document objects.
    """

    def __init__(
        self,
        content_field: str,
        metadata_fields: Optional[List[str]] = None,
        custom_transform: Optional[Callable[[Dict[str, Any]], Document]] = None,
    ):
        self.content_field = content_field
        self.metadata_fields = metadata_fields or []
        self.custom_transform = custom_transform

    def transform_record(self, record: Dict[str, Any]) -> Document:
        """
        Convert a single record into a Document.

        Raises:
            ValueError: If transformation fails
        """
        try:
            if self.custom_transform:
                return self.custom_transform(record)

            content = str(record.get(self.content_field, ""))

            metadata = {
                field: record.get(field)
                for field in self.metadata_fields
                if field in record
            }

            return Document(page_content=content, metadata=metadata)

        except Exception as e:
            raise ValueError(f"Error transforming record: {record}") from e

    def transform_batch(self, records: List[Dict[str, Any]]) -> List[Document]:
        """
        Convert multiple records into Documents.
        """
        documents = []

        for record in records:
            try:
                doc = self.transform_record(record)
                documents.append(doc)
            except Exception as e:
                print(f"⚠️ Skipping record due to error: {e}")

        return documents



# Dynamic Transformer (Schema-Agnostic)

class DynamicDocumentTransformer(DocumentTransformer):
    """
    Automatically adapts to unknown schema.
    """

    def __init__(self):
        super().__init__(content_field="")

    def transform_record(self, record: Dict[str, Any]) -> Document:
        try:
            # Convert values to string (handle ObjectId etc.)
            safe_record = {k: str(v) for k, v in record.items()}

            content = " | ".join(f"{k}: {v}" for k, v in safe_record.items())

            metadata = {
                "_id": safe_record.get("_id"),
            }

            return Document(page_content=content, metadata=metadata)

        except Exception as e:
            raise ValueError(f"Dynamic transform failed for record: {record}") from e



# Converter

class CollectionToDocumentConverter:
    """
    Converts collection data into LangChain Documents.
    Supports batch & streaming conversion.
    """

    def __init__(self, transformer: DocumentTransformer):
        self.transformer = transformer

    def convert(self, data: List[Dict[str, Any]]) -> List[Document]:
        """
        Convert full dataset into documents.
        """
        if not data:
            return []

        try:
            return self.transformer.transform_batch(data)
        except Exception as e:
            raise RuntimeError("Batch conversion failed") from e

    def convert_stream(self, records: Iterable[Dict[str, Any]]):
        """
        Stream conversion (memory efficient).

        Yields:
            Document
        """
        for record in records:
            try:
                yield self.transformer.transform_record(record)
            except Exception as e:
                print(f"⚠️ Skipping record in stream due to error: {e}")