"""
Factory module for vector storage services.

Provides a function to initialize and return a vector storage instance
based on the storage type specified in the configuration.
"""


from ai_agent.config import VectorStoreConfig
from ai_agent.infrastructure.embedding_model import get_embedding_model
from ai_agent.infrastructure.sql_storage.postgresql import PostgreSQLStorage

from .chroma import ChromaVectorStorage
from .postgres import PostgresVectorStorage

embedding_function = get_embedding_model()


def get_vector_storage():
    """
    Return a storage instance based on the STORAGE_TYPE config value.

    Returns:
        BaseVectorStore: An implementation of the vector storage interface.
    """
    if VectorStoreConfig.provider.lower() == "chroma":
        return ChromaVectorStorage(VectorStoreConfig, embedding_function)
    if VectorStoreConfig.provider.lower() == "postgresql":
        sql_storage = PostgreSQLStorage(VectorStoreConfig)
        return PostgresVectorStorage(VectorStoreConfig, embedding_function, sql_storage)
    raise ValueError(f"Unsupported vector storage type: {VectorStoreConfig.storage_type}")
