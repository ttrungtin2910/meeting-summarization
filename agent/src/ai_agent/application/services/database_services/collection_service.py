"""
Collection Service Module
"""

from datetime import datetime, timezone
from typing import List
from uuid import UUID

from ai_agent.domain.dtos.collection_dto import (CollectionCreateDTO,
                                                 CollectionCreateRequestDTO,
                                                 CollectionUpdateDTO)
from ai_agent.domain.exceptions.collection_exceptions import (
    CollectionAlreadyExists, CollectionInUseError, CollectionNotFound)
from ai_agent.domain.models.database_entities.collection import Collection
from ai_agent.domain.models.security_contexts.organization_context import \
    OrganizationContext
from ai_agent.infrastructure.database.repositories import (
    BaseCategoryRepository, BaseCollectionRepository,
    BaseOrganizationRepository)


class CollectionService:
    """
    Service for managing collection operations.

    This service class provides business logic for collection-related operations
    such as creation, retrieval, and management, serving as an intermediary between
    the API layer and the repository layer.
    """
    def __init__(
            self,
            collection_repository: BaseCollectionRepository,
            category_repository: BaseCategoryRepository,
            organization_repository: BaseOrganizationRepository
        ):
        """
        Initialize the collection service with a repository.

        Args:
            collection_repository (BaseCollectionRepository): Repository for collection data access
            category_repository (BaseCategoryRepository): Repository for category data access
            organization_repository (BaseOrganizationRepository): repository for organization table
        """
        self.collection_repository = collection_repository
        self.category_repository = category_repository
        self.organization_repository = organization_repository

    def create_collection(
            self,
            organization_context: OrganizationContext,
            data: CollectionCreateRequestDTO
        ) -> Collection:
        """
        Creates a new collection for the current client.

        Args:
            organization_context (OrganizationContext): The authenticated organization
            data (CollectionCreateRequestDTO): The details of the collection to
                be created.

        Returns:
            Collection: The newly created collection.

        Raises:
            CollectionAlreadyExists: If a collection with the same name already
                exists within the client's organization.
        """
        organization_id = organization_context.organization_id

        # Check organization with the same name exists
        collection_name = data.name
        database_collection = self.collection_repository.get_by_name(
            collection_name,
            organization_id=organization_id
        )

        if database_collection:
            raise CollectionAlreadyExists(name=collection_name)

        # Create DTO
        collection_dto = CollectionCreateDTO(
            **data.model_dump(),
            created_at=datetime.now(tz=timezone.utc)
        )

        new_collection = self.collection_repository.create(
            collection_dto,
            organization_id=organization_id
        )
        return new_collection

    def get_collection(
            self,
            collection_id: UUID,
            organization_context: OrganizationContext,
        ) -> Collection:
        """
        Get a collection.

        Args:
            collection_id (UUID)
            organization_context (OrganizationContext): The authenticated organization

        Returns:
            Collection

        Raises:
            CollectionNotFound: If the collection with the given ID does not exist
        """
        organization_id = organization_context.organization_id

        collection = self.collection_repository.get_by_id(
            collection_id,
            organization_id=organization_id
        )
        if not collection:
            raise CollectionNotFound(collection_id=collection_id)
        return collection

    def get_list_collections(
            self,
            organization_context: OrganizationContext,
        ) -> List[Collection]:
        """
        Get list of all collections.

        Args:
            organization_context (OrganizationContext): The authenticated organization

        Returns:
            List[Collection]

        Raises:
            CollectionNotFound: If the collection with the given ID does not exist
        """
        organization_id = organization_context.organization_id

        collections = self.collection_repository.get_list(organization_id=organization_id)
        return collections

    def update_collection(
            self,
            collection_id: UUID,
            data: CollectionUpdateDTO,
            organization_context: OrganizationContext,
        ) -> Collection:
        """
        Update an existing collection.

        Args:
            collection_id (UUID): ID of the collection that needs to update
            data (UpdateCollectionDTO): DTO containing the updated collection information
                - name (str)
            organization_context (OrganizationContext): The authenticated organization

        Returns:
            Collection: The updated collection object

        Raises:
            CollectionNotFound: If the collection with the given ID does not exist
        """
        organization_id = organization_context.organization_id

        collection = self.collection_repository.get_by_id(
            collection_id,
            organization_id=organization_id
        )
        if not collection:
            raise CollectionNotFound(collection_id=collection_id)

        # Check if no field changed compared to the existed collection
        has_changed = False
        update_data = data.model_dump(exclude_unset=True, exclude_none=True)
        for field, new_value in update_data.items():
            old_value = getattr(collection, field, None)
            if new_value != old_value:
                has_changed = True
                break

        # If no change, return the original collection
        if not has_changed:
            return collection

        # If has change
        updated_collection = self.collection_repository.update(
            collection_id,
            data,
            organization_id=organization_id
        )
        assert updated_collection is not None
        return updated_collection

    def delete_collection(
            self,
            collection_id: UUID,
            organization_context: OrganizationContext,
        ) -> None:
        """
        Delete a collection.

        Args:
            collection_id (UUID): ID of the collection
            organization_context (OrganizationContext): The authenticated organization

        Returns:
            None

        Raises:
            CollectionNotFound: If the collection with the given ID does not exist
            CollectionInUseError: the collection still has associated categories
        """
        organization_id = organization_context.organization_id

        # Check if collection exists
        collection = self.collection_repository.get_by_id(
            collection_id,
            organization_id=organization_id
        )
        if not collection:
            raise CollectionNotFound(collection_id=collection_id)

        # Check if associated category exists
        categories = self.category_repository.get_list(
            collection_id=collection_id,
            organization_id=organization_id
        )
        if categories:
            raise CollectionInUseError(collection_id=collection_id)

        self.collection_repository.delete(
            collection_id,
            organization_id=organization_id
        )
