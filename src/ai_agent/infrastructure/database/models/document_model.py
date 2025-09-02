"""
Defines the Document ORM model for managing document metadata.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ai_agent.domain.value_objects.document_status import DocumentStatus
from ai_agent.infrastructure.database.base.base_model import Base


class DocumentModel(Base):
    """
    ORM model representing a document record stored in the database.
    """

    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)

    storage_uri = Column(String(255), nullable=False, unique=True)

    created_at = Column(
        DateTime,
        default=datetime.now(tz=timezone.utc),
        nullable=False
    )

    updated_at = Column(
        DateTime,
        default=datetime.now(tz=timezone.utc),
        onupdate=datetime.now(tz=timezone.utc),
        nullable=False
    )

    status: Mapped[DocumentStatus] = mapped_column(
        Enum(DocumentStatus),
        default=DocumentStatus.PENDING,
        nullable=False
    )

    organization_id = Column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id"),
        nullable=False
    )

    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True)
    category = relationship("CategoryModel", backref="documents")
