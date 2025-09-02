"""
Category DTO
"""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class CategoryCreateRequestDTO(BaseModel):
    """
    Model to create a new category, from API to application.

    Attributes:
        name (str): Name of the collection
        collection_id (UUID): ID of the collection the category belongs to
    """
    name: str
    collection_id: UUID


class CategoryCreateDTO(BaseModel):
    """
    Model to create a new category, from application to infrastructure.

    Attributes:
        name (str): Name of the collection
        collection_id (UUID): ID of the collection the category belongs to
        created_at (datetime): The timestamp when the category was created
    """
    name: str
    collection_id: UUID
    created_at: datetime


class CategoryUpdateDTO(BaseModel):
    """
    Model to update a collection.

    Attributes:
        name (Optional[str]): Name of the category
    """
    name: Optional[str] = None

    class Config:
        """Config to map data"""
        from_attributes = True
