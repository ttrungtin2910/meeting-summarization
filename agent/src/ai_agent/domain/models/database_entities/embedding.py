"""
Embedding Model Module
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from ai_agent.domain.models.database_entities.document import Document


class Embedding(BaseModel):
    """
    Embedding data model.

    Attributes:
        id (UUID): Unique identifier for the embedding.
        content (str): Text content of the chunk.
        document_id (UUID): ID of the document the embedding is created from.
        document (Document): Full document metadata.
        created_at (datetime): Timestamp when the embedding was created.
    """

    id: UUID
    content: str
    document_id: UUID
    document: Document
    created_at: datetime

    class Config:
        """Config to allow mapping from ORM"""
        from_attributes = True
