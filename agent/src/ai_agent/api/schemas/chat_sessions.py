"""Models for chat session API"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from ai_agent.api.schemas.chat import ChatResponse
from ai_agent.api.schemas.collections import CollectionResponse


class ChatSessionResponse(BaseModel):
    """
    Represents the response for a chat session retrieval request.

    Attributes:
        id (UUID): ID of the chat session.
        name (Optional[str]): Name/title of the chat session.
        external_user_id (UUID): ID of the user who owns the session.
        collections (List[CollectionResponse]) ID of the collections
            the chat_session belongs to
        created_at (datetime): Timestamp of when the session was created.
    """

    id: UUID
    name: Optional[str] = None
    external_user_id: UUID
    client_id: UUID
    organization_id: UUID
    collections: List[CollectionResponse]
    created_at: datetime

    history_messages: List[ChatResponse]

    class Config:
        """Enable ORM mapping"""
        from_attributes = True


class ChatSessionCreateRequest(BaseModel):
    """
    Schema for creating a new chat session.

    Attributes:
        name (str): Title of the chat session.
        user_id (UUID): ID of the user who owns the session.
    """

    name: str = Field(..., max_length=100, description="Name of the chat session")
    user_id: UUID = Field(..., description="ID of the user who owns the session")


class ChatSessionUpdate(BaseModel):
    """
    Schema for updating a chat session.

    Attributes:
        name (Optional[str]): New title of the chat session.
    """

    name: Optional[str] = Field(
        None,
        max_length=100,
        description="Updated name of the chat session"
    )
