"""Models for documents API"""

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from .categories import CategoryMinimalResponse


class DocumentResponse(BaseModel):
    """
    Represents the response for a document retrieval request.

    Attributes:
        id (UUID): Id of the document
        name (str): Name of the document
        category (CategoryMinimalResponse): category the document belongs to
    """
    id: UUID
    name: str
    category: CategoryMinimalResponse

    class Config:
        """Config class for mapping data"""
        from_attributes = True


class DocumentUpdate(BaseModel):
    """Schema for updating a collection."""
    name: Optional[str] = Field(None, max_length=100, description="Name of the document")
    category_id: Optional[UUID] = Field(None, description="ID of the category the document belongs to")
