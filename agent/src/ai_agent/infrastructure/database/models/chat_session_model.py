"""
Defines the Chat Session ORM model
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ai_agent.infrastructure.database.base.base_model import Base

from .chat_session_collection_model import chat_session_collection_model


class ChatSessionModel(Base):
    """
    ORM model representing a chat session
    """

    __tablename__ = "chat_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.now(tz=timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(tz=timezone.utc), nullable=False)

    external_user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("external_users.id"),
        nullable=False,
        doc="Reference to the external user"
    )

    client_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("app_clients.client_id"),
        nullable=False,
        doc="Reference to the associated app client"
    )

    collections: Mapped[list["CollectionModel"]] = relationship(
        "CollectionModel",
        secondary=chat_session_collection_model,
        back_populates="chat_sessions",
        doc="Collections the chat session can access"
    )

    organization_id = Column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id"),
        nullable=False
    )
