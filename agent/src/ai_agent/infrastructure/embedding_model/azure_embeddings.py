"""
Embedding model implementation.

Provides the AzureOpenAIEmbeddings class, which initializes and
returns an AzureOpenAIEmbeddings instance based on provided configuration.
"""

from langchain_openai import AzureOpenAIEmbeddings

from .base import BaseEmbeddingModel


class AzureOpenAIEmbeddingsModel(BaseEmbeddingModel):
    """
    Embedding model implementation using Azure's embedding API.
    It inherits from BaseEmbeddingModel
    """
    def __init__(self, config):
        """
        Initialize the AzureOpenAIEmbeddings with the provided configuration.

        Args:
            config: a configuration object containing required keys:
                - "api_key": Your OpenAI API key.
                - "model": Name of the embedding model to use.
        """
        self.api_key = config.api_key
        self.endpoint = config.endpoint
        self.version = config.version
        self.model = config.model

    def get_model(self) -> AzureOpenAIEmbeddings:
        """
        Return an instance of AzureOpenAIEmbeddings initialized with the current configuration.

        return: An instance of AzureOpenAIEmbeddings from LangChain.
        """
        return AzureOpenAIEmbeddings(
            api_key=self.api_key,
            azure_endpoint=self.endpoint,
            api_version=self.version,
            azure_deployment=self.model
        )
