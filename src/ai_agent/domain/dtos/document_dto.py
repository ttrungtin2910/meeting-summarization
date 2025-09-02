"""
Document DTO
"""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from ai_agent.domain.value_objects.document_status import DocumentStatus


class DocumentCreateRequestDTO(BaseModel):
    """
    Data Transfer Object for creating a new document, from API to Application.

    Attributes:
        custom_name (str): The name provided by user
        filename (str): The name of the document uploaded
        storage_uri (str): The URI where the document is stored
        category_id (UUID): The unique identifier of the category this document belongs to
    """
    custom_name: str
    filename: str
    storage_uri: str
    category_id: UUID


class DocumentCreateDTO(BaseModel):
    """
    Data Transfer Object for creating a new document, from Application to Infrastructure.

    Attributes:
        name (str): the name of the provided document
        storage_uri (str): The URI where the document is stored
        category_id (UUID): The unique identifier of the category this document belongs to
        created_at (datetime): The timestamp of when the document was created
        updated_at (datetime): The timestamp of when the document was last updated
    """
    name: str
    storage_uri: str
    category_id: UUID
    created_at: datetime
    updated_at: datetime


class DocumentUpdateDTO(BaseModel):
    """
    Data Transfer Object for updating an existing document.

    Attributes:
        storage_uri (Optional[str]): The updated URI where the document is stored
        status (Optional[DocumentStatus]): The updated status of the document
        category_id (Optional[UUID]): The ID of the category the document belongs to
        updated_at (Optional[datetime]):  The timestamp of when the document was last updated
    """
    name: Optional[str] = None
    status: Optional[DocumentStatus] = None
    category_id: Optional[UUID] = None
    updated_at: Optional[datetime] = None

    class Config:
        """Config to map data"""
        from_attributes = True
