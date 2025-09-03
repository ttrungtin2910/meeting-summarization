"""
Defines the Embedding ORM model for storing vector embeddings and metadata.
"""

import uuid
from datetime import datetime, timezone

from pgvector.sqlalchemy import Vector  # type: ignore
from sqlalchemy import Column, DateTime, ForeignKey, Index, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ai_agent.infrastructure.database.base.base_model import Base


class EmbeddingModel(Base):
    """
    ORM model representing a stored vector embedding with metadata.
    """

    __tablename__ = "embeddings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False)
    document = relationship("DocumentModel", backref="embeddings")
    created_at = Column(DateTime, default=datetime.now(tz=timezone.utc), nullable=False)

    content = Column(Text, nullable=False)
    embedding: Mapped[list[float]] = mapped_column(Vector(1536))

    organization_id = Column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id"),
        nullable=False
    )

    __table_args__ = (
        Index(
            "ix_embeddings_vector",
            "embedding",
            postgresql_using="hnsw",
            postgresql_ops={"embedding": "vector_cosine_ops"},
            postgresql_with={"m": "16", "ef_construction": "200"},
        ),
    )
