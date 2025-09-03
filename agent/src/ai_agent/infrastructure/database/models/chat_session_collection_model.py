"""
This module defines the association table for chat sessions and collections.
"""

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID

from ai_agent.infrastructure.database.base.base_model import Base

chat_session_collection_model = Table(
    "chat_session_collection",
    Base.metadata,
    Column(
        "chat_session_id",
        UUID(as_uuid=True),
        ForeignKey("chat_sessions.id"),
        primary_key=True
    ),
    Column(
        "collection_id",
        UUID(as_uuid=True),
        ForeignKey("collections.id"),
        primary_key=True
    ),
)
