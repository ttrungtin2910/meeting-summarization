"""
openai_embedder.py

Provides an implementation of BaseEmbedder using OpenAI's embedding API.
"""

from typing import List

from langchain_openai import OpenAIEmbeddings

from .base import BaseEmbedder


class OpenAIEmbedder(BaseEmbedder):
    """
    Embedding model implementation using OpenAI's embedding API.
    Inherits from BaseEmbedder.
    """

    def __init__(self, config):
        """
        Initialize the OpenAIEmbedder with an OpenAIEmbeddings model.

        Args:
            config: Object with:
                - api_key (str)
                - model (str)
        """
        self.model = OpenAIEmbeddings(
            api_key=config.api_key,
            model=config.model
        )

    def embed_text(self, text: str) -> List[float]:
        """
        Convert a single string of text into an embedding vector.
        """
        return self.model.embed_query(text)

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Convert a list of text strings into embedding vectors.
        """
        return self.model.embed_documents(texts)
