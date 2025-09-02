"""
Repository for Category model.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from ai_agent.domain.dtos.category_dto import (CategoryCreateDTO,
                                               CategoryUpdateDTO)
from ai_agent.domain.models.database_entities.category import Category


class BaseCategoryRepository(ABC):
    """
    Abstract base repository class for managing Category model operations.

    This abstract class defines the interface for Category repositories,
    providing methods for CRUD operations on Category entities.
    """

    @abstractmethod
    def create(
        self,
        data: CategoryCreateDTO,
        organization_id: UUID
    ) -> Category:
        """
        Create a new category.

        Args:
            data (CategoryCreateDTO): The data required to create the category,
                including:
                - name (str): The name of the category.
                - collection_id (UUID): The ID of the collection to which the category belongs.
                - created_at (datetime): the timestamp when the category was created
            organization_id (UUID): Id of organization

        Returns:
            Category: The newly created category object.
        """

    @abstractmethod
    def get_by_id(
        self,
        category_id: UUID,
        organization_id: UUID
    ) -> Optional[Category]:
        """
        Retrieve a category by its ID.

        Args:
            category_id (UUID): The UUID of the category to retrieve
            organization_id (UUID): Id of organization

        Returns:
            Optional[Category]: The category if found, None otherwise
        """

    @abstractmethod
    def get_by_name(
        self,
        category_name: str,
        collection_id: UUID,
        organization_id: UUID
    ) -> Optional[Category]:
        """
        Retrieve a category by its name.

        Args:
            category_name (str): The name of the category to retrieve
            collection_id (UUID): The ID of the collection that the category belongs to
            organization_id (UUID): Id of organization

        Returns:
            Optional[Category]: The category if found, None otherwise
        """

    @abstractmethod
    def get_list(
        self,
        collection_id: UUID,
        organization_id: UUID
    ) -> List[Category]:
        """
        Retrieve all categories for a specific collection.

        Args:
            collection_id (UUID): The UUID of the collection to get categories for
            organization_id (UUID): Id of organization

        Returns:
            List[Category]: A list of all category objects in the collection
        """

    @abstractmethod
    def delete(
        self,
        category_id: UUID,
        organization_id: UUID
    ) -> None:
        """
        Delete a category by its ID.

        Args:
            category_id (UUID): The UUID of the category to delete
            organization_id (UUID): Id of organization

        Returns:
            None
        """

    @abstractmethod
    def update(
        self,
        category_id: UUID,
        data: CategoryUpdateDTO,
        organization_id: UUID
    ) -> Optional[Category]:
        """
        Update a category with new data.

        Args:
            category_id (UUID): The UUID of the category to update.
            data (CategoryUpdateDTO): The fields to update the category with,
                including (optionally):
                - name (str): The new name of the category.
            organization_id (UUID): Id of organization

        Returns:
            Optional[Category]: The updated category object if found, otherwise None.
        """
