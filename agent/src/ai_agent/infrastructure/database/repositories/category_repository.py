"""
Repository for Category model.
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from ai_agent.domain.dtos.category_dto import (CategoryCreateDTO,
                                               CategoryUpdateDTO)
from ai_agent.domain.models.database_entities.category import Category
from ai_agent.infrastructure.database.models import CategoryModel

from .base_category_repository import BaseCategoryRepository


class CategoryRepository(BaseCategoryRepository):
    """
    Repository class for managing Category model operations in the database.

    This class provides methods to create, retrieve, list, and delete Category entities.
    """

    def __init__(self, session: Session):
        """
        Initialize the CategoryRepository with a database session.

        Args:
            session (Session): database session
        """
        self.session = session

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
        category = CategoryModel(
            **data.model_dump(),
            organization_id=organization_id
        )

        self.session.add(category)
        self.session.commit()
        self.session.refresh(category)

        return Category.model_validate(category)

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
        result = (
            self.session
            .query(CategoryModel)
            .filter(
                CategoryModel.id == category_id,
                CategoryModel.organization_id == organization_id
            )
            .first()
        )

        if not result:
            return None
        return Category.model_validate(result)

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
        result =  (
            self.session.query(CategoryModel)
            .filter(
                CategoryModel.name == category_name,
                CategoryModel.collection_id == collection_id,
                CategoryModel.organization_id == organization_id
            )
            .first()
        )

        if not result:
            return None
        return Category.model_validate(result)

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
        results = (
            self.session
            .query(CategoryModel)
            .filter(
                CategoryModel.collection_id == collection_id,
                CategoryModel.organization_id == organization_id
            )
            .all()
        )

        if len(results) == 0:
            return []
        return [Category.model_validate(result) for result in results]

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
        category = (
            self.session.query(CategoryModel)
            .filter(
                CategoryModel.id == category_id,
                CategoryModel.organization_id == organization_id
            )
            .first()
        )
        if category:
            self.session.delete(category)
            self.session.commit()

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
        category = (
            self.session.query(CategoryModel)
            .filter(
                CategoryModel.id == category_id,
                CategoryModel.organization_id == organization_id
            )
            .first()
        )

        if not category:
            return None

        update_data = data.model_dump(exclude_unset=True, exclude_none=True)
        for key, value in update_data.items():
            setattr(category, key, value)

        self.session.commit()
        self.session.refresh(category)

        return Category.model_validate(category)
