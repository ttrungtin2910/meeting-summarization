"""
Chat Session module
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from ai_agent.domain.models.database_entities.collection import Collection
from ai_agent.domain.models.database_entities.history_message import \
    HistoryMessage


class ChatSession(BaseModel):
    """
    Domain ChatSession model.

    Attributes:
        id (UUID): Unique identifier for the ChatSession
        name (Optional[str]): Name of the session

        external_user_id (UUID): ID of the external user
        client_id (UUID): ID of the client the user belongs to

        collections (List[Collection]): Collections the chat session belongs to
        organization_id (UUID): ID of the organization the user belongs to

        created_at (datetime): Timestamp when the session was created
        updated_at (datetime): Timestamp when the session was updated
    """
    id: UUID
    name: Optional[str] = None

    external_user_id: UUID
    client_id: UUID

    collections: List[Collection]
    organization_id: UUID

    created_at: datetime
    updated_at: datetime

    history_messages: List[HistoryMessage]

    class Config:
        """Config to map data"""
        from_attributes = True

