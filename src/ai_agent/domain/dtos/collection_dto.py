"""
Collection DTO
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CollectionCreateRequestDTO(BaseModel):
    """
    Model to create a new collection.

    Attributes:
        name (str): Name of the collection
    """
    name: str


class CollectionCreateDTO(BaseModel):
    """
    Model to create a new collection.

    Attributes:
        name (str): Name of the collection
        created_at (datetime): The timestamp when the collection was created
    """
    name: str
    created_at: datetime


class CollectionUpdateDTO(BaseModel):
    """
    Model to update a collection.

    Attributes:
        name (Optional[str]): Name of the collection
    """
    name: Optional[str] = None
