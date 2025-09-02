"""
Category Service Module.
"""

from datetime import datetime, timezone
from typing import List
from uuid import UUID

from ai_agent.domain.dtos.category_dto import (CategoryCreateDTO,
                                               CategoryCreateRequestDTO,
                                               CategoryUpdateDTO)
from ai_agent.domain.exceptions.category_exceptions import (
    CategoryAlreadyExists, CategoryInUseError, CategoryNotFound)
from ai_agent.domain.exceptions.collection_exceptions import CollectionNotFound
from ai_agent.domain.models.database_entities.category import Category
from ai_agent.domain.models.security_contexts.organization_context import \
    OrganizationContext
from ai_agent.infrastructure.database.repositories import (
    BaseCategoryRepository, BaseCollectionRepository, BaseDocumentRepository,
    BaseOrganizationRepository)


class CategoryService:
    """
    Service class for managing category operations.

    This service encapsulates business logic for category management,
    utilizing the repository pattern for data access.
    """

    def __init__(
            self,
            category_repository: BaseCategoryRepository,
            collection_repository: BaseCollectionRepository,
            document_repository: BaseDocumentRepository,
            organization_repository: BaseOrganizationRepository,
        ):
        """
        Initialize the CategoryService with a category repository.

        Args:
            category_repository (BaseCategoryRepository): An implementation of the
                BaseCategoryRepository interface used for data access operations.
            collection_repository (BaseCollectionRepository): repository for collection table
            document_repository (BaseDocumentRepository): repository for document table
            organization_repository (BaseOrganizationRepository): repository for organization table
        """
        self.category_repository = category_repository
        self.collection_repository = collection_repository
        self.document_repository = document_repository
        self.organization_repository = organization_repository

    def create_category(
            self,
            data: CategoryCreateRequestDTO,
            organization_context: OrganizationContext
        ) -> Category:
        """
        Create a new category.

        Args:
            data (CategoryCreateRequestDTO): The category create object, containing:
                - name (str)
                - collection_id (UUID)
            organization_context (OrganizationContext): The authenticated organization context

        Returns:
            Category: The newly created category object with assigned ID.

        Raises:
            CollectionNotFound: If the collection with the given ID does not exist
            CategoryAlreadyExists: If the category name is already exists.
        """
        organization_id = organization_context.organization_id
        category_name = data.name
        collection_id = data.collection_id

        # Check if the specified collection exists
        collection = self.collection_repository.get_by_id(
            collection_id=collection_id,
            organization_id=organization_id
        )
        if not collection:
            raise CollectionNotFound(collection_id)

        # Check if a category with the same name already exists in the collection
        existed_category = self.category_repository.get_by_name(
            category_name=category_name,
            collection_id=collection_id,
            organization_id=organization_id
        )

        if existed_category:
            raise CategoryAlreadyExists(category_name, collection_id)

        # create dto
        category_dto = CategoryCreateDTO(
            **data.model_dump(),
            created_at = datetime.now(tz=timezone.utc)
        )

        # Create the new category
        new_category = self.category_repository.create(
            category_dto,
            organization_id=organization_id
        )
        return new_category

    def get_category(
            self,
            category_id: UUID,
            organization_context: OrganizationContext
        ) -> Category:
        """
        Retrieve a single category by its ID.

        Args:
            category_id (UUID): The ID of the category to retrieve.
            organization_context (OrganizationContext): The authenticated organization context

        Returns:
            Category: The retrieved category object.

        Raises:
            CategoryNotFound: If no category with the given ID exists.
        """
        organization_id = organization_context.organization_id
        category = self.category_repository.get_by_id(
            category_id,
            organization_id=organization_id
        )
        if not category:
            raise CategoryNotFound(category_id)
        return category

    def get_list_categories(
            self,
            collection_id: UUID,
            organization_context: OrganizationContext
        ) -> List[Category]:
        """
        Retrieve all categories belonging to a specific collection.

        Args:
            collection_id (UUID): The ID of the collection.
            organization_context (OrganizationContext): The authenticated organization context

        Returns:
            List[Category]: A list of category objects in the specified collection.

        Raises:
            CollectionNotFound: If the collection does not exist.
        """
        organization_id = organization_context.organization_id
        if not self.collection_repository.exists(
            collection_id=collection_id,
            organization_id=organization_id
        ):
            raise CollectionNotFound(collection_id=collection_id)

        categories = self.category_repository.get_list(
            collection_id,
            organization_id=organization_id
        )
        return categories

    def update_category(
            self,
            category_id: UUID,
            data: CategoryUpdateDTO,
            organization_context: OrganizationContext
        ) -> Category:
        """
        Update an existing category.

        Args:
            category_id (UUID): The ID of the category to update.
            data (CategoryUpdateDTO): Data for updating the category (e.g., name).
            organization_context (OrganizationContext): The authenticated organization context

        Returns:
            Category: The updated category object.

        Raises:
            CategoryNotFound: If the category does not exist.
            CategoryAlreadyExists: If another category with the same name
                already exists in the same collection.
        """
        organization_id = organization_context.organization_id
        category = self.category_repository.get_by_id(
            category_id,
            organization_id=organization_id
        )
        if not category:
            raise CategoryNotFound(category_id)

        # Check if no field changed compared to the existed category
        has_changed = False
        update_data = data.model_dump(exclude_unset=True, exclude_none=True)
        for field, new_value in update_data.items():
            old_value = getattr(category, field, None)
            if new_value != old_value:
                has_changed = True
                break

        # If no change, return the original collection
        if not has_changed:
            return category

        # Check name uniqueness if name is being updated
        collection_id = category.collection.id if category.collection else None
        if data.name and collection_id:
            existed_category = self.category_repository.get_by_name(
                category_name=data.name,
                collection_id=collection_id,
                organization_id=organization_id
            )
            if existed_category and existed_category.id != category_id:
                raise CategoryAlreadyExists(data.name, collection_id)

        updated_category = self.category_repository.update(
            category_id,
            data,
            organization_id=organization_id
        )
        assert updated_category is not None
        return updated_category

    def delete_category(
            self,
            category_id: UUID,
            organization_context: OrganizationContext
        ) -> None:
        """
        Delete a category by its ID.

        Args:
            category_id (UUID): The ID of the category to delete.
            organization_context (OrganizationContext): The authenticated organization context

        Raises:
            CategoryNotFound: If the category does not exist.
        """
        organization_id = organization_context.organization_id
        category = self.category_repository.get_by_id(
            category_id,
            organization_id=organization_id
        )
        if not category:
            raise CategoryNotFound(category_id)

        # Check if associated documents exist
        documents = self.document_repository.get_list(
            category_id=category_id,
            organization_id=organization_id
        )
        if documents:
            raise CategoryInUseError(category_id)

        self.category_repository.delete(
            category_id,
            organization_id=organization_id
        )
