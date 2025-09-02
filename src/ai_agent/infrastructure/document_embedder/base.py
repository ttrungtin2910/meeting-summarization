"""
Base interface for document embedder.

This module defines the abstract base class for document embedding services
that convert text into vector representations for use in search and retrieval systems.
"""

from abc import ABC, abstractmethod
from typing import List


class BaseEmbedder(ABC):
    """
    Abstract base class for text embedding services.


    Implementations of this interface should handle the process of converting
    text strings into numerical vectors
    """
    @abstractmethod
    def embed_text(self, text: str) -> List[float]:
        """
        Convert text into a vector embedding.

        This method transforms a given text string into a numerical vector representation
        that captures its semantic meaning, allowing for similarity comparisons with
        other embedded texts.

        Args:
            text (str): The text to be embedded

        Returns:
            List[float]: A vector representation of the input text
                as a list of floating-point numbers
        """

    @abstractmethod
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Convert a list of texts into embeddings.

        Args:
            texts (List[str]): The texts to be embedded

        Returns:
            List[List[float]]: A list of vector representations
        """
