"""
Document splitting base class.

Provides the base interface for document splitters that break Document
into smaller chunks.
"""

from abc import ABC, abstractmethod
from typing import List

from ai_agent.domain.value_objects.retrieval_document import RetrievalDocument


class BaseSplitter(ABC):
    """
    Abstract base class for text splitters.

    All custom splitters should inherit from this class and implement the `split_documents` method.
    """

    @abstractmethod
    def split_documents(self, retrieval_documents: List[RetrievalDocument]) -> List[RetrievalDocument]:
        """
        Split a list of documents into smaller chunks.

        Args:
            retrieval_documents (List[RetrievalDocument]): The input documents to be split.

        Returns:
            List[RetrievalDocument]: A list of chunked documents.
        """
