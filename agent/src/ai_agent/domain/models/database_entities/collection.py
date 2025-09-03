"""
Collection Model Module
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class Collection(BaseModel):
    """
    Collection data model.

    Attributes:
        id (UUID): Unique identifier for the collection
        name (str): Name of the collection
        created_at (datetime): Timestamp when the collection was created
    """
    id: UUID
    name: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        """Config to map data"""
        from_attributes = True
