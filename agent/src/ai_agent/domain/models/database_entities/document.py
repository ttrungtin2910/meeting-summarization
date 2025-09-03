"""
Document Model Module
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from ai_agent.domain.models.database_entities.category import Category
from ai_agent.domain.value_objects.document_status import DocumentStatus


class Document(BaseModel):
    """
    Document data model.

    Attributes:
        id (UUID): Unique identifier for the collection
        name (str): Name of the collection
        storage_uri (str):  A string representing the URI where the document is stored
        created_at (datetime): Timestamp when the collection was created
        updated_at (datetime): Timestamp when the collection was updated
        status (DocumentStatus): status of document, used to decide sync or not
        category_id (UUID): ID of the category the document belongs to
        category (Category): Category that the document belongs to
    """
    id: UUID
    name: str
    storage_uri: str

    created_at: datetime
    updated_at: datetime

    status: DocumentStatus
    category_id: UUID
    category: Category

    class Config:
        """Config to map data"""
        from_attributes = True
