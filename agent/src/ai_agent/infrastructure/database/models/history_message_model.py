"""
Defines the history chat Message model
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ai_agent.domain.value_objects.chat_message import ChatRole
from ai_agent.infrastructure.database.base.base_model import Base


class HistoryMessageModel(Base):
    """
    ORM model representing a History Chat message
    """

    __tablename__ = "history_messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("chat_sessions.id"), nullable=False)
    session = relationship(
        "ChatSessionModel",
        backref="history_messages"
    )
    type: Mapped[ChatRole] = mapped_column(
        Enum(ChatRole),
        nullable=False
    )
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now(tz=timezone.utc), nullable=False)

    organization_id = Column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id"),
        nullable=False
    )
