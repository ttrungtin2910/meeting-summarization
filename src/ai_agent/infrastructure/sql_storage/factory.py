"""
Factory module for SQL storage services.

Provides a function to initialize and return a SQL storage instance
based on the configured storage type.
"""

from ai_agent.config import SQLStorageConfig

from .base import BaseSQLStorage
from .postgresql import PostgreSQLStorage


def get_sql_storage() -> BaseSQLStorage:
    """
    Factory function that creates and returns an appropriate SQL storage instance
    based on configuration.

    This function examines the SQLStorageConfig.STORAGE_TYPE setting and instantiates
    the corresponding storage implementation.

    Returns:
        An instance of a SQL storage implementation (e.g., PostgreSQLStorage)

    Raises:
        ValueError: If SQLStorageConfig.STORAGE_TYPE is not supported
    """

    if SQLStorageConfig.storage_type.lower() == "postgres":
        return PostgreSQLStorage(SQLStorageConfig)

    raise ValueError(f"Unsupported vector storage type: {SQLStorageConfig.storage_type}")
