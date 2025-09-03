"""
Model for the Admin table.

This model defines system administrators who are allowed
to perform privileged actions such as creating organizations.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from ai_agent.infrastructure.database.base.base_model import Base


class AdminModel(Base):
    """
    Represents an administrator of the platform.

    Admins are allowed to perform global operations such as
    creating organizations.

    Attributes:
        id: Unique identifier for the admin (UUID).
        Name: Email used for authentication.
        hashed_password: Securely hashed password.
        created_at: Timestamp when the admin was created.
    """
    __tablename__ = "admins"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(tz=timezone.utc),
        nullable=False
    )
