"""Models for Sync API"""

from uuid import UUID

from pydantic import BaseModel


class SyncResponse(BaseModel):
    """
    Response schema for document synchronization operations.


    Attributes:
        collection_id (UUID): The unique identifier of the collection that was synchronized
        added (int): The number of new documents added to the collection. Defaults to 0.
        deleted (int): The number of documents deleted from the collection. Defaults to 0.
        updated (int): The number of documents updated in the collection. Defaults to 0.
    """
    collection_id: UUID
    added: int = 0
    deleted: int = 0
    updated: int = 0

    class Config:
        """Config class for mapping data"""
        from_attributes = True
