"""
Factory module for storage.

Provides a function to initialize and return a configured Storage
based on the provider specified in the StorageConfig.
"""

from ai_agent.config import StorageConfig

from .azure_blob_storage import AzureBlobStorage


def get_storage():
    """
    Return a storage instance based on the STORAGE_TYPE config value.

    Returns:
        BaseStorageService: An implementation of the storage interface.
    """
    if StorageConfig.storage_type == "azure":
        return AzureBlobStorage(StorageConfig)
    else:
        raise ValueError(f"Unsupported storage type: {StorageConfig.storage_type}")
