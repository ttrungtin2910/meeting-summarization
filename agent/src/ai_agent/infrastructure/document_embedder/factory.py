"""
Factory module for initializing embedding models.

Provides a function to select and return an embedding model instance
based on the configured provider.
"""

from ai_agent.config import EmbeddingConfig

from .azure_embedder import AzureEmbedder
from .openai_embedder import OpenAIEmbedder


def get_embedder():
    """
    Factory function to initialize and return the configured embedder instance.

    This function reads the embedding provider from `EmbeddingConfig.PROVIDER` and
    initializes the corresponding embedder.

    Returns:
        An instance of the selected embedder class.

    Raises:
        ValueError: If the specified provider in EmbeddingConfig.PROVIDER is not supported.
    """
    provider = EmbeddingConfig.provider.lower()

    # OpenAI
    if provider == "openai":
        return OpenAIEmbedder(EmbeddingConfig)

    # Azure OpenAI
    if provider == "azure":
        return AzureEmbedder(EmbeddingConfig)

    # Unsupported
    raise ValueError(f"Unsupported embedder provider: {EmbeddingConfig.provider}")
