"""
Defines the ORM model for App Clients.

AppClient represents an external system authorized to call API.
Each client is linked to an organization.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, relationship

from ai_agent.infrastructure.database.base.base_model import Base

from .app_client_collection_model import app_client_collection_model


class AppClientModel(Base):
    """
    SQLAlchemy model representing an app client for API access.
    """

    __tablename__ = "app_clients"

    client_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_secret = Column(String, nullable=False)

    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    is_active = Column(Boolean, default=True, nullable=False)

    collections: Mapped[list["CollectionModel"]] = relationship(
        "CollectionModel",
        secondary=app_client_collection_model,
        back_populates="app_clients",
        doc="Collections the app client can access"
    )

    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
