"""
Embedding model implementation.

Provides the OpenAIEmbeddingsModel class, which initializes and
returns an OpenAIEmbeddings instance based on provided configuration.
"""

from langchain_openai import OpenAIEmbeddings

from .base import BaseEmbeddingModel


class OpenAIEmbeddingsModel(BaseEmbeddingModel):
    """
    Embedding model implementation using OpenAI's embedding API.
    It inherits from BaseEmbeddingModel
    """
    def __init__(self, config):
        """
        Initialize the OpenAIEmbeddingsModel with the provided configuration.

        Args:
            config: a configuration object containing required keys:
                - "api_key": Your OpenAI API key.
                - "model": Name of the embedding model to use.
        """
        self.api_key = config.api_key
        self.model = config.model

    def get_model(self) -> OpenAIEmbeddings:
        """
        Return an instance of OpenAIEmbeddings initialized with the current configuration.

        return: An instance of OpenAIEmbeddings from LangChain.
        """
        return OpenAIEmbeddings(
            api_key=self.api_key,
            model=self.model,
        )
