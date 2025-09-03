"""
History message module
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from ai_agent.domain.value_objects.chat_message import ChatRole


class HistoryMessage(BaseModel):
    """
    History Message model.

    Attributes:
        id (UUID): Unique identifier for the ChatSession
        type (ChatRole): Role of the message: ai, user, system
        content (str): Message content
        session_id (UUID): ID of the session that the message belongs to
        created_at (datetime): Timestamp when the session was created
    """
    id: UUID
    type: ChatRole
    content: str
    session_id: UUID
    created_at: datetime

    class Config:
        """Config to map data"""
        from_attributes = True
