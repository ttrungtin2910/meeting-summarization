"""
Document Service Module.

This service encapsulates business logic for document management, such as creating,
retrieving, updating, deleting, and syncing documents to the embedding system.
"""

from datetime import datetime, timedelta, timezone
from typing import List, Optional
from uuid import UUID

from ai_agent.domain.dtos.document_dto import (DocumentCreateDTO,
                                               DocumentCreateRequestDTO,
                                               DocumentUpdateDTO)
from ai_agent.domain.dtos.download_dto import DownloadInfoDTO
from ai_agent.domain.exceptions.category_exceptions import CategoryNotFound
from ai_agent.domain.exceptions.collection_exceptions import CollectionNotFound
from ai_agent.domain.exceptions.document_exceptions import (DocumentDeleted,
                                                            DocumentNotFound)
from ai_agent.domain.models.database_entities.document import Document
from ai_agent.domain.models.security_contexts.organization_context import \
    OrganizationContext
from ai_agent.domain.value_objects.document_status import DocumentStatus
from ai_agent.infrastructure.database.repositories import (
    BaseCategoryRepository, BaseCollectionRepository, BaseDocumentRepository,
    BaseOrganizationRepository)
from ai_agent.infrastructure.storage.base import BaseStorage
from ai_agent.utilities.file_utils import delete_file
from ai_agent.utilities.url_utils import add_extension, build_remote_path


class DocumentService:
    """
    Service class for managing document operations.
    """

    def __init__(
        self,
        collection_repository: BaseCollectionRepository,
        category_repository: BaseCategoryRepository,
        document_repository: BaseDocumentRepository,
        organization_repository: BaseOrganizationRepository,
        storage: BaseStorage,
        expire_minutes: int = 15
    ):
        """
        Initialize the DocumentService with a document repository

        Args:
            collection_repository (BaseCollectionRepository): Repository for collection data access.
            document_repository (BaseDocumentRepository): Interface to access documents.
            category_repository (BaseCategoryRepository): Interface to access categories.
            organization_repository (BaseOrganizationRepository): repository for organization table
            storage (BaseStorage): Access the storage service for uploading and downloading files.
            expire_minutes (int):
                The number of minutes after which the download link for the document will expire.
        """
        self.collection_repository = collection_repository
        self.document_repository = document_repository
        self.category_repository = category_repository
        self.organization_repository = organization_repository
        self.storage = storage
        self.expire_minutes = expire_minutes

    def create_document(
            self,
            data: DocumentCreateRequestDTO,
            organization_context: OrganizationContext,
        ) -> Document:
        """
        Create a new document.

        Args:
            data (DocumentCreateDTO): Data to create the document.
            organization_context (OrganizationContext): The authenticated organization

        Returns:
            Document: The created document.

        Raises:
            CategoryNotFound: If the category with the given ID does not exist
        """
        # Check if the category exists
        organization_id = organization_context.organization_id
        category_id: UUID = data.category_id
        category = self.category_repository.get_by_id(
            category_id,
            organization_id=organization_id
        )

        if not category:
            raise CategoryNotFound(category_id=category_id)

        # Build remote path
        filename = add_extension(data.custom_name, data.filename)
        collection_id = category.collection.id
        remote_path = build_remote_path(
            filename,
            collection_id,
            category_id,
            organization_id=organization_id
        )

        # Upload to blob and update URL
        local_path: str = data.storage_uri
        self.storage.upload(local_path=local_path, remote_path=remote_path)

        # Delete local file
        delete_file(local_path)

        # Create DTO object
        document_dto = DocumentCreateDTO(
            name=filename,
            storage_uri=remote_path,
            category_id=category_id,
            created_at = datetime.now(tz=timezone.utc),
            updated_at = datetime.now(tz=timezone.utc)
        )

        # Save to table
        return self.document_repository.create(
            document_dto,
            organization_id=organization_id
        )

    def get_list_documents(
            self,
            organization_context: OrganizationContext,
            collection_id: Optional[UUID] = None,
            category_id: Optional[UUID] = None
        ) -> List[Document]:
        """
        Retrieve a list of documents from a specific collection and optionally filtered by category.

        This method fetches documents from the repository based on the provided collection ID
        and optional category ID. It validates that the collection exists, and if a category ID
        is provided, it also validates that the category exists before retrieving the documents.

        Args:
            collection_id (Optional[UUID]): The ID of the collection to get documents from
            category_id (Optional[UUID], optional): The category ID to filter documents by.
                Defaults to None.
            organization_context (OrganizationContext): The authenticated organization

        Returns:
            List[Document]: A list of document objects matching the query criteria

        Raises:
            CollectionNotFound: If no collection exists with the provided collection_id
            CategoryNotFound: If a category_id is provided but no category exists with that ID
        """
        # Check if collection exists
        organization_id = organization_context.organization_id
        if collection_id:
            collection = self.collection_repository.get_by_id(
                collection_id,
                organization_id=organization_id
            )
            if not collection:
                raise CollectionNotFound(collection_id)

        # If have category filter, check if category exists
        if category_id:
            category = self.category_repository.get_by_id(
                category_id,
                organization_id=organization_id
            )
            if not category:
                raise CategoryNotFound(category_id)

        return self.document_repository.get_list(
            collection_id=collection_id,
            category_id=category_id,
            organization_id=organization_id
        )

    def get_document(
            self,
            document_id: UUID,
            organization_context: OrganizationContext,
        ):
        """
        Retrieve a specific document by its ID.

        This method fetches a single document from the repository based on the provided
        document ID. It validates that the document exists before returning it.

        Args:
            document_id (UUID): The unique identifier of the document to retrieve
            organization_context (OrganizationContext): The authenticated organization

        Returns:
            Document: The document object if found

        Raises:
            DocumentNotFound: If no document exists with the provided document_id
        """
        organization_id = organization_context.organization_id
        document = self.document_repository.get(
            document_id,
            organization_id=organization_id
        )
        if not document:
            raise DocumentNotFound(document_id)
        return document

    def download_document(
            self,
            document_id: UUID,
            organization_context: OrganizationContext,
        ) -> DownloadInfoDTO:
        """
        Generate a download URL for a specific document.

        This method retrieves a document by its ID, generates a temporary download URL
        for the document from the storage service, and returns download information
        including the URL and its expiration time.

        Args:
            document_id (UUID): The unique identifier of the document to download
            organization_context (OrganizationContext): The authenticated organization

        Returns:
            DownloadInfo: An object containing the document name,
                download URL, and URL expiration time

        Raises:
            DocumentNotFound: If no document exists with the provided document_id
        """
        document = self.get_document(
            document_id,
            organization_context=organization_context
        )
        if not document:
            raise DocumentNotFound(document_id)
        download_url = self.storage.generate_download_url(document.storage_uri)

        return DownloadInfoDTO(
            name=document.name,
            url=download_url,
            expires_at=datetime.now(tz=timezone.utc) + timedelta(minutes=self.expire_minutes)
        )

    def delete_document(
            self,
            document_id: UUID,
            organization_context: OrganizationContext,
        ) -> None:
        """
        Delete a document by its ID

        Args:
            document_id (UUID)
            organization_context (OrganizationContext): The authenticated organization

        Returns:
            None

        Raises:
            DocumentNotFound: If the document with the given ID does not exist
        """
        organization_id = organization_context.organization_id
        document = self.document_repository.get(
            document_id,
            organization_id=organization_id
        )

        if not document:
            raise DocumentNotFound(document_id=document_id)

        # Delete data in the table
        self.document_repository.delete(
            document_id,
            organization_id=organization_id
        )
        # Delete data in blob
        self.storage.delete(document.storage_uri)

    def soft_delete_document(
            self,
            document_id: UUID,
            organization_context: OrganizationContext,
        ) -> None:
        """
        Soft delete a document by setting is_deleted = True and deleted_at = now.

        Args:
            document_id (UUID): ID of the document to soft-delete.
            organization_context (OrganizationContext): The authenticated organization

        Raises:
            DocumentNotFound: If the document does not exist (or already deleted).
            DocumentDeleted: If the document is already in the deleted state.
        """
        organization_id = organization_context.organization_id
        document = self.document_repository.get(
            document_id,
            organization_id=organization_id
        )

        if not document:
            raise DocumentNotFound(document_id=document_id)

        # Check if status is Deleted
        if document.status == DocumentStatus.DELETED:
            raise DocumentDeleted(document_id=document_id)

        # Update status of the document
        update_dto = DocumentUpdateDTO(
            status=DocumentStatus.DELETED,
            updated_at=datetime.now(tz=timezone.utc)
        )
        self.document_repository.update(
            document_id,
            update_dto,
            organization_id=organization_id
        )

    def update_document(
            self,
            document_id: UUID,
            data: DocumentUpdateDTO,
            organization_context: OrganizationContext,
        ) -> Document:
        """
        Update an existing document.

        Args:
            document_id (UUID): The ID of the document to update.
            data (DocumentUpdateDTO): Data for updating the document (e.g., name).
            organization_context (OrganizationContext): The authenticated organization

        Returns:
            Document: The updated document object.

        Raises:
            DocumentNotFound: If the document does not exist.
            DocumentAlreadyExists: If another document with the same name
                already exists in the same collection.
        """
        organization_id = organization_context.organization_id
        document = self.document_repository.get(
            document_id,
            organization_id=organization_id
        )
        if not document:
            raise DocumentNotFound(document_id)

        # Add extension if update name
        if data.name:
            data.name = add_extension(data.name, document.name)

        # Check if category_id exists in the current collection
        if data.category_id and data.category_id != document.category_id:
            old_category = self.category_repository.get_by_id(
                document.category_id,
                organization_id=organization_id
            )
            assert old_category is not None

            new_category = self.category_repository.get_by_id(
                data.category_id,
                organization_id=organization_id
            )
            if not new_category or new_category.collection_id != old_category.collection_id:
                raise CategoryNotFound(data.category_id)

        # Check if no field changed compared to the existed document
        has_changed = False
        update_data = data.model_dump(exclude_unset=True, exclude_none=True)
        for field, new_value in update_data.items():
            old_value = getattr(document, field, None)
            if new_value != old_value:
                has_changed = True
                break

        # If no change, return the original document
        if not has_changed:
            return document

        # If has change
        data.updated_at = datetime.now(tz=timezone.utc)
        updated_document = self.document_repository.update(
            document_id,
            data,
            organization_id=organization_id
        )
        assert updated_document is not None
        return updated_document
