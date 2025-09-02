"""
azure_embedder.py

Provides an implementation using Azure OpenAI's embedding API.
"""

from typing import List

from langchain_openai import AzureOpenAIEmbeddings

from .base import BaseEmbedder


class AzureEmbedder(BaseEmbedder):
    """
    Embedding model implementation using Azure's embedding API.
    """

    def __init__(self, config):
        """
        Initialize the AzureEmbedder with AzureOpenAIEmbeddings model.

        Args:
            config: Object with:
                - api_key (str)
                - endpoint (str)
                - version (str)
                - model (str)
        """
        self.model = AzureOpenAIEmbeddings(
            api_key=config.api_key,
            api_version=config.version,
            azure_endpoint=config.endpoint,
            azure_deployment=config.model
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
