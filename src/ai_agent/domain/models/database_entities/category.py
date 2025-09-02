"""
Category Model Module
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from ai_agent.domain.models.database_entities.collection import Collection


class Category(BaseModel):
    """
    Category data model.

    Attributes:
        id (UUID): Unique identifier for the collection
        name (str): Name of the collection
        created_at (datetime): Timestamp when the collection was created
        collection_id (UUID): ID of the collection that the category belongs to
        collection (Optional[Collection]): collection that the category belongs to
    """
    id: UUID
    name: str
    created_at: datetime

    collection_id: UUID
    collection: Collection

    class Config:
        """Config to map data"""
        from_attributes = True
