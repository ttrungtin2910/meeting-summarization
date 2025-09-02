"""
DTOs for HistoryMessage operations.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from ai_agent.domain.value_objects.chat_message import ChatRole


class HistoryMessageCreateRequestDTO(BaseModel):
    """
    Request DTO for creating a history message (from API).

    Attributes:
        session_id (UUID): ID of the chat session.
        type (ChatRole): Role (e.g., user, assistant).
        content (str): Message content.
    """
    session_id: UUID
    type: ChatRole
    content: str


class HistoryMessageCreateDTO(BaseModel):
    """
    Internal DTO for creating a history message (used by service → repository).

    Attributes:
        session_id (UUID): ID of the chat session.
        type (ChatRole): Role of the message.
        content (str): Message content.
        created_at (datetime): Time the message was created.
    """
    session_id: UUID
    type: ChatRole
    content: str
    created_at: datetime
