"""
Organization database model module.

This module defines the SQLAlchemy ORM model for organization entities
in the database
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from ai_agent.infrastructure.database.base.base_model import Base


class OrganizationModel(Base):
    """
    Database model representing an organization.

    This model defines the structure of the organizations table in the database,
    storing essential information about organizations in the system.

    Attributes:
        id (UUID): The unique identifier for the organization
        name (String): The name of the organization
        hashed_password (String): The hashed password for the organization
        is_active (Boolean): whether the organization active or not
        created_at (DateTime): The timestamp when the organization was created

    Table:
        organizations: The database table storing organization records
    """
    __tablename__ = "organizations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )
    created_at = Column(DateTime, default=datetime.now(tz=timezone.utc))
