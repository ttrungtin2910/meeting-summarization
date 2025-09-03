"""
Repository interface for managing Document entities.

This module defines the abstract interface for document persistence operations
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from ai_agent.domain.dtos.document_dto import (DocumentCreateDTO,
                                               DocumentUpdateDTO)
from ai_agent.domain.models.database_entities.document import Document


class BaseDocumentRepository(ABC):
    """
    Abstract base class for document repository operations.

    Defines a set of methods for working with documents in a persistent store.
    """

    @abstractmethod
    def create(
        self,
        data: DocumentCreateDTO,
        organization_id: UUID
    ) -> Document:
        """
        Create a new document.

        Args:
            data (DocumentCreateDTO): Data used to create the document.
            organization_id (UUID): ID of the organization

        Returns:
            Document: The newly created document entity.
        """

    @abstractmethod
    def get(
        self,
        document_id: UUID,
        organization_id: UUID
    ) -> Optional[Document]:
        """
        Retrieve a document by its ID.

        Args:
            document_id (UUID): The ID of the document.
            organization_id (UUID): ID of the organization

        Returns:
            Optional[Document]: The document if found, else None.
        """

    @abstractmethod
    def get_list(
        self,
        organization_id: UUID,
        collection_id: Optional[UUID] = None,
        category_id: Optional[UUID] = None,
    ) -> List[Document]:
        """
        Retrieve a list of documents, optionally filtered by collection or category.

        Args:
            organization_id (UUID): ID of the organization
            collection_id (Optional[UUID]): The ID of the collection to filter by.
            category_id (Optional[UUID]): The ID of the category to filter by.

        Returns:
            List[Document]: A list of matching documents.
        """

    @abstractmethod
    def update(
        self,
        document_id: UUID,
        data: DocumentUpdateDTO,
        organization_id: UUID
    ) -> Optional[Document]:
        """
        Update a document with new data.

        Args:
            document_id (UUID): The ID of the document to update.
            data (DocumentUpdateDTO): Fields to update.
            organization_id (UUID): ID of the organization

        Returns:
            Optional[Document]: The updated document, or None if not found.
        """

    @abstractmethod
    def delete(
        self,
        document_id: UUID,
        organization_id: UUID
    ) -> None:
        """
        Delete a document by its ID.

        Args:
            document_id (UUID): The ID of the document to delete.
            organization_id (UUID): ID of the organization
        """
