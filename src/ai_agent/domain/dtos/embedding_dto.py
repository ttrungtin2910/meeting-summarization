"""
Embedding Create DTO Module
"""

from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, Field


class EmbeddingCreateDTO(BaseModel):
    """
    DTO for creating a new embedding.

    Attributes:
        content (str): Raw text chunk to be embedded.
        embedding (List[float]): Vector representation of the content.
        document_id (UUID): Document ID to which this embedding belongs.
        created_at (datetime): The timestamp when the embedding was created
    """

    content: str = Field(..., description="The raw text content of the chunk.")
    embedding: List[float] = Field(..., description="The vector embedding of the content.")
    document_id: UUID = Field(..., description="The document this embedding is linked to.")
    created_at: datetime = Field(..., description="The timestamp when the embedding was created")

    class Config:
        """Map data from attributes of other class"""
        from_attributes = True


class EmbeddingCreateRequestDTO(BaseModel):
    """
    DTO for creating a new embedding, sending to application layer.

    Attributes:
        content (str): Raw text chunk to be embedded.
        embedding (List[float]): Vector representation of the content.
        document_id (UUID): Document ID to which this embedding belongs.
    """

    content: str = Field(..., description="The raw text content of the chunk.")
    embedding: List[float] = Field(..., description="The vector embedding of the content.")
    document_id: UUID = Field(..., description="The document this embedding is linked to.")
