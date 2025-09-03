"""
Category API schemas.

This module defines the models for category API request and response validation.
These schemas handle data validation and serialization for the category endpoints.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from .collections import CollectionResponse


class CategoryCreate(BaseModel):
    """Schema for category creation request."""
    name: str = Field(..., min_length=1, max_length=100, description="Name of the category")


class CategoryUpdate(BaseModel):
    """Schema for updating a Category."""
    name: str = Field(..., min_length=1, max_length=100, description="Name of the category")


class CategoryResponse(BaseModel):
    """Schema for category response."""
    id: UUID
    name: str
    created_at: datetime

    collection: CollectionResponse

    class Config:
        """Pydantic configuration for ORM mode."""
        from_attributes = True


class CategoryMinimalResponse(BaseModel):
    """Schema for category minimal response."""
    id: UUID
    name: str
    created_at: datetime

    class Config:
        """Pydantic configuration for ORM mode."""
        from_attributes = True
