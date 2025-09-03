"""
Base interface for vector storage services.

Defines the BaseVectorStore abstract class with common methods
for adding documents, performing similarity search, and document management.
"""


from abc import ABC, abstractmethod
from typing import Any, List

from langchain.schema import Document


class BaseVectorStore(ABC):
    """
    Abstract base class for a vector store.
    """
    @abstractmethod
    def add_documents(self, documents: List[Document]) -> None:
        """Add list of LangChain Documents to the vector store."""

    @abstractmethod
    def similarity_search(self, query: str, k: int = 5) -> List[Any]:
        """
        Perform similarity search.
        """

    @abstractmethod
    def as_retriever(self):
        """
        Return a retriever-compatible object.
        """

    @abstractmethod
    def get_documents(self, filters: dict):
        """
        Get documents.
        """

    @abstractmethod
    def delete_documents(self, filters: dict):
        """
        Delete documents based on a metadata
        """
