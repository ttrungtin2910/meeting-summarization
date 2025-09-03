"""
Base interface for embedding models.
"""

from abc import ABC, abstractmethod


class BaseEmbeddingModel(ABC):
    """
    Interface for embedding models.
    """
    @abstractmethod
    def get_model(self):
        """Return the initialized embedding instance"""
