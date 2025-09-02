"""
Collection API schemas.

This module defines the models for collection API
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class CollectionCreate(BaseModel):
    """Schema for collection creation request."""
    name: str = Field(..., min_length=1, max_length=100, description="Name of the collection")


class CollectionUpdate(BaseModel):
    """Schema for updating a collection."""
    name: str = Field(..., min_length=1, max_length=100, description="Name of the collection")


class CollectionResponse(BaseModel):
    """Schema for collection response."""
    id: UUID
    name: str
    created_at: datetime

    class Config:
        """configuration for ORM mode."""
        from_attributes = True
