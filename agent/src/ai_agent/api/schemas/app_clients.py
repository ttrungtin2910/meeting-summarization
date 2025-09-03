"""
Schemas for AppClient API responses.
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from .collections import CollectionResponse

class AppClientResponse(BaseModel):
    """
    Schema for returning AppClient data to clients
    """
    client_id: UUID
    client_secret: str
    name: str
    collection_ids: List[UUID]
    collections: List[CollectionResponse]
    is_active: bool
    created_at: datetime

    class Config:
        """Config for mapping data"""
        from_attributes = True


class AppClientCreateResponse(BaseModel):
    """
    Schema for returning AppClient data to clients
    when creating the app client
    """
    client_id: UUID
    client_secret: str
    name: str
    collection_ids: List[UUID]
    is_active: bool
    created_at: datetime

    class Config:
        """Config for mapping data"""
        from_attributes = True


class AppClientCreateRequest(BaseModel):
    """
    Schema for creating new AppClient

    Attributes:
        name (str): The name of the AppClient.
        collection_ids (List[UUID]): List of collections ID
    """
    name: str
    collection_ids: List[UUID]


class AppClientUpdate(BaseModel):
    """
    Schema for updating an existing AppClient.

    All fields are optional, allowing for partial updates.

    Attributes:
        name (Optional[str]): The new name of the AppClient, if it is to be updated.
        collection_ids (List[UUID]): List of collections ID
    """
    name: Optional[str] = None
    collection_ids: List[UUID]

