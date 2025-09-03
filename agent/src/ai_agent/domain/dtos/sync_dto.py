"""DTO for sending sync information to Response API"""

from pydantic import BaseModel


class SyncResponseDTO(BaseModel):
    """
    Data transfer object for document synchronization operations.


    Attributes:
        added (int): The number of new documents added to the collection. Defaults to 0.
        deleted (int): The number of documents deleted from the collection. Defaults to 0.
        updated (int): The number of documents updated in the collection. Defaults to 0.
    """
    added: int = 0
    deleted: int = 0
    updated: int = 0

    class Config:
        """Config class for mapping data"""
        from_attributes = True
