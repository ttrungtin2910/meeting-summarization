"""
Defines the domain model for AppClient.
"""

from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel

from ai_agent.api.schemas.collections import CollectionResponse

class AppClient(BaseModel):
    """
    Domain model representing an AppClient used for authentication and authorization.
    """
    client_id: UUID
    client_secret: str
    name: str
    organization_id: UUID
    collection_ids: List[UUID]
    collections: List[CollectionResponse]
    is_active: bool = True
    created_at: datetime

    @classmethod
    def from_db_model(cls, db_model) -> "AppClient":
        """
        Creates an AppClient instance from a database model.

        Args:
            db_model: The database model containing client data.

        Returns:
            AppClient: An instance populated with data from the db_model.
        """
        return cls(
            client_id = db_model.client_id,
            client_secret = db_model.client_secret,
            name = db_model.name,
            organization_id = db_model.organization_id,
            collection_ids = [collection.id for collection in db_model.collections],
            collections = db_model.collections,
            is_active = db_model.is_active,
            created_at = db_model.created_at
        )


    class Config:
        """Config class for mapping data"""
        from_attributes = True
