"""
Defines the External user ORM model
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from ai_agent.infrastructure.database.base.base_model import Base


class ExternalUserModel(Base):
    """
    model for external users associated with app clients.
    Each external user belongs to an organization and a client.
    """

    __tablename__ = "external_users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    external_user: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        doc="External system-provided user identifier"
    )

    client_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("app_clients.client_id"),
        nullable=False,
        doc="Reference to the app client created the external user"
    )

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id"),
        nullable=False,
        doc="Reference to the owning organization"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        doc="Timestamp of creation"
    )
