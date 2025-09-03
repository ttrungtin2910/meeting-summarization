"""
Data Transfer Objects (DTOs) for creating and updating AppClient.
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class AppClientCreateRequestDTO(BaseModel):
    """
    DTO for creating a new AppClient, from API to service

    Attributes:
        name (str): The name of the AppClient.
        collection_ids (List[UUID]): IDs of collections to chat with
    """
    name: str
    collection_ids: List[UUID]

    class Config:
        """Config class for mapping data"""
        from_attributes = True


class AppClientCreateDTO(BaseModel):
    """
    DTO for creating a new AppClient.

    Attributes:
        client_id (UUID): The unique identifier for the AppClient.
        client_secret (str): The secret key associated with the AppClient.
        name (str): The name of the AppClient.
        collection_ids (List(UUID)): ID of collections to chat with
        is_active (bool): Indicates whether the AppClient is active. Defaults to True.
        created_at (datetime): The timestamp when the AppClient was created.
    """
    client_id: UUID
    client_secret: str
    name: str
    collection_ids: List[UUID]
    is_active: bool = True
    created_at: datetime


class AppClientUpdateDTO(BaseModel):
    """
    DTO for updating an existing AppClient.

    All fields are optional, allowing for partial updates.

    Attributes:
        name (Optional[str]): The new name of the AppClient, if it is to be updated.
        collection_ids (Optional[List[UUID]]): ID of collections to chat with
        is_active (Optional[bool]): The active status of the AppClient, if it is to be updated.
    """
    name: Optional[str] = None
    collection_ids: Optional[List[UUID]] = None
    is_active: Optional[bool] = None

    class Config:
        """Config class for mapping data"""
        from_attributes = True
