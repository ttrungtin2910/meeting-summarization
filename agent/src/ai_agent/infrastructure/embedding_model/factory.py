"""
Factory module for initializing embedding models.

Provides a function to select and return an embedding model instance
based on the configured provider.
"""

from ai_agent.config import EmbeddingConfig

from .azure_embeddings import AzureOpenAIEmbeddingsModel
from .openai_embeddings import OpenAIEmbeddingsModel


def get_embedding_model():
    """
    Factory function to initialize and return the configured embedding model instance.

    This function reads the embedding provider from `EmbeddingConfig.PROVIDER` and
    initializes the corresponding embedding model.

    Returns:
        An instance of the selected embedding model class.

    Raises:
        ValueError: If the specified provider in EmbeddingConfig.PROVIDER is not supported.
    """
    provider = EmbeddingConfig.provider.lower()

    # OpenAI
    if provider == "openai":
        model_instance = OpenAIEmbeddingsModel(EmbeddingConfig)
        return model_instance.get_model()

    # Azure OpenAI
    elif provider == "azure":
        model_instance = AzureOpenAIEmbeddingsModel(EmbeddingConfig)
        return model_instance.get_model()

    # Unsupported
    raise ValueError(f"Unsupported embedding model provider: {EmbeddingConfig.provider}")
