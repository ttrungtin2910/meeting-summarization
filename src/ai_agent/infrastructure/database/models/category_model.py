"""
Defines the Category ORM model for classifying documents into categories.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ai_agent.infrastructure.database.base.base_model import Base


class CategoryModel(Base):
    """
    Model representing a category for classifying documents.
    """

    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.now(tz=timezone.utc), nullable=False)

    collection_id = Column(UUID(as_uuid=True), ForeignKey("collections.id"), nullable=False)
    collection = relationship("CollectionModel", backref="categories")
    organization_id = Column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id"),
        nullable=False
    )
