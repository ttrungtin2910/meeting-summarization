"""
Chat Session DTO
"""
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class ChatSessionCreateRequestDTO(BaseModel):
    """
    DTO for creating a new chat session.

    This class represents the data required to create a new chat session,
    including the user identifier who owns the session.

    Attributes:
        external_user (str): The identifier of the external user creating the chat session
        collection_id (Optional[List[UUID]]]): IDs of the collections to retrieve for RAG
    """
    external_user: str
    collection_ids: Optional[List[UUID]] = None


class ChatSessionCreateDTO(BaseModel):
    """
    DTO for creating a new chat session.

    This class represents the data required to create a new chat session,
    including the chat session name and the user who owns it.

    Attributes:
        name (Optional[str]): The name of the chat session
        external_user_id (UUID): ID of the external user
        collection_ids (List[UUID]): IDs of the collections to retrieve for RAG
        client_id (UUID): ID of client
        organization_id (UUID): ID of organization
        created_at (Optional[datetime]): The timestamp the session is created
        updated_at (Optional[datetime]): The timestamp the session is updated
    """
    name: Optional[str] = None
    external_user_id: UUID
    collection_ids: List[UUID]
    client_id: UUID
    organization_id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ChatSessionUpdateDTO(BaseModel):
    """
    DTO for updating an existing chat session.

    This class represents the data that can be updated for an existing chat session.
    All fields are optional since updates may be partial.

    Attributes:
        name (str): The new name for the chat session
    """
    name: str

    class Config:
        """Config to map data"""
        from_attributes = True
