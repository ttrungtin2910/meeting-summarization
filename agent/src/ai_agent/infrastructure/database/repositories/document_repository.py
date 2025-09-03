"""
Repository class for managing Document entities in the database.
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from ai_agent.domain.dtos.document_dto import (DocumentCreateDTO,
                                               DocumentUpdateDTO)
from ai_agent.domain.models.database_entities.document import Document
from ai_agent.domain.value_objects.document_status import DocumentStatus
from ai_agent.infrastructure.database.models import DocumentModel
from ai_agent.infrastructure.database.models.category_model import \
    CategoryModel

from .base_document_repository import BaseDocumentRepository


class DocumentRepository(BaseDocumentRepository):
    """
    Implementation of BaseDocumentRepository.

    Handles all document-related data persistence logic using the database session provided.
    """

    def __init__(self, session: Session):
        """
        Initialize the repository with a SQLAlchemy session.

        Args:
            session (Session): Database session.
        """
        self.session = session

    def create(
            self,
            data: DocumentCreateDTO,
            organization_id: UUID
        ) -> Document:
        """
        Create a new document in the database.

        Args:
            data (DocumentCreateDTO): Data used to create the document.
            organization_id (UUID): ID of the organization

        Returns:
            Document: The newly created document entity.
        """
        document = DocumentModel(
            **data.model_dump(),
            organization_id=organization_id
        )
        document.status = DocumentStatus.PENDING
        self.session.add(document)
        self.session.commit()
        self.session.refresh(document)
        return Document.model_validate(document)

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
        document = (
            self.session
            .query(DocumentModel)
            .filter(
                DocumentModel.id == document_id,
                DocumentModel.organization_id == organization_id
            )
            .first()
        )
        if not document:
            return None
        return Document.model_validate(document)

    def get_list(
        self,
        organization_id: UUID,
        collection_id: Optional[UUID] = None,
        category_id: Optional[UUID] = None,
    ) -> List[Document]:
        """
        Retrieve a list of documents filtered by optional collection or category.

        Args:
            organization_id (UUID): ID of the organization
            collection_id (Optional[UUID]): The collection to filter by.
            category_id (Optional[UUID]): The category to filter by.

        Returns:
            List[Document]: List of matching documents.
        """
        query = self.session.query(DocumentModel)

        if collection_id:
            # Join category to filter through collection
            query = query.join(CategoryModel, DocumentModel.category_id == CategoryModel.id)
            query = query.filter(
                CategoryModel.collection_id == collection_id,
                CategoryModel.organization_id == organization_id
            )

        if category_id:
            query = query.filter(
                DocumentModel.category_id == category_id,
                DocumentModel.organization_id == organization_id
            )

        return [Document.model_validate(d) for d in query.all()]

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
            data (DocumentUpdateDTO): The fields to update.
            organization_id (UUID): ID of the organization

        Returns:
            Optional[Document]: The updated document, or None if not found.
        """
        document = (
            self.session
            .query(DocumentModel)
            .filter(
                DocumentModel.id == document_id,
                DocumentModel.organization_id == organization_id
            )
            .first()
        )

        if not document:
            return None

        update_data = data.model_dump(exclude_unset=True, exclude_none=True)
        for key, value in update_data.items():
            setattr(document, key, value)
        self.session.commit()
        self.session.refresh(document)
        return Document.model_validate(document)

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
        document = (
            self.session
            .query(DocumentModel)
            .filter_by(
                id=document_id,
                organization_id=organization_id
            )
            .first()
        )
        if document:
            self.session.delete(document)
            self.session.commit()
