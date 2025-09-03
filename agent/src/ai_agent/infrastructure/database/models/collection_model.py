"""
Defines the Collection ORM model for grouping documents and embeddings.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, relationship

from ai_agent.infrastructure.database.base.base_model import Base

from .app_client_collection_model import app_client_collection_model
from .chat_session_collection_model import chat_session_collection_model


class CollectionModel(Base):
    """
    ORM model representing a collection for grouping related documents and embeddings.
    """

    __tablename__ = "collections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.now(tz=timezone.utc), nullable=False)

    app_clients: Mapped[list["AppClientModel"]] = relationship(
        "AppClientModel",
        secondary=app_client_collection_model,
        back_populates="collections"
    )

    chat_sessions: Mapped[list["ChatSessionModel"]] = relationship(
        "ChatSessionModel",
        secondary=chat_session_collection_model,
        back_populates="collections"
    )

    organization_id = Column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id"),
        nullable=False
    )
