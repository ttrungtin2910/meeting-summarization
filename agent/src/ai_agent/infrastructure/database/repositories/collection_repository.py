"""
Repository for Collection model.
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session
from yaml import CollectionNode

from ai_agent.domain.dtos.collection_dto import (CollectionCreateDTO,
                                                 CollectionUpdateDTO)
from ai_agent.domain.models.database_entities.collection import Collection
from ai_agent.infrastructure.database.models import CollectionModel

from .base_collection_repository import BaseCollectionRepository


class CollectionRepository(BaseCollectionRepository):
    """
    Repository class for managing Collection model operations in the database.

    This class provides methods to create, retrieve, list, update, and delete Collection entities.
    """

    def __init__(self, session: Session):
        """
        Initialize the CollectionRepository with a database session.

        Args:
            session (Session): SQLAlchemy database session
        """
        self.session = session

    def create(
        self,
        data: CollectionCreateDTO,
        organization_id: UUID
    ) -> Collection:
        """
        Create a new collection.

        Args:
            data (CollectionCreateDTO): The data required to create a collection.
                - name (str): The name of the collection.
            organization_id (UUID): ID of the organization

        Returns:
            Collection: The newly created collection object.
        """
        # Convert DTO to ORM model
        collection = CollectionModel(
            **data.model_dump(),
            organization_id=organization_id
        )

        self.session.add(collection)
        self.session.commit()
        self.session.refresh(collection)

        return Collection.model_validate(collection)

    def get_by_id(
        self,
        collection_id: UUID,
        organization_id: UUID
    ) -> Optional[Collection]:
        """
        Retrieve a collection by its ID.

        Args:
            collection_id (UUID): The UUID of the collection to retrieve
            organization_id (UUID): ID of the organization

        Returns:
            Optional[collection]: The collection if found, None otherwise
        """
        collection = (
            self.session.query(CollectionModel)
            .filter(
                CollectionModel.id==collection_id,
                CollectionModel.organization_id==organization_id
            )
            .first()
        )
        if collection is None:
            return None
        return Collection.model_validate(collection)

    def get_by_name(
        self,
        collection_name: str,
        organization_id: UUID
    ) -> Optional[Collection]:
        """
        Retrieve a collection by its name.

        Args:
            collection_name (str): The name of the collection to retrieve
            organization_id (UUID): ID of the organization

        Returns:
            Optional[collection]: The collection if found, None otherwise
        """
        collection = (
            self.session.query(CollectionModel)
            .filter(
                CollectionModel.name == collection_name,
                CollectionModel.organization_id==organization_id
            )
            .first()
        )
        if collection is None:
            return None
        return Collection.model_validate(collection)

    def get_list(
        self,
        organization_id: UUID
    ) -> List[Collection]:
        """
        Retrieve all categories.

        Args:
            organization_id (UUID): ID of the organization

        Returns:
            List[collection]: A list of all collection objects
        """
        collections = (
            self.session
            .query(CollectionModel)
            .filter(CollectionModel.organization_id==organization_id)
            .all())
        if len(collections) == 0:
            return []
        return [Collection.model_validate(collection) for collection in collections]

    def delete(
        self,
        collection_id: UUID,
        organization_id: UUID
    ) -> None:
        """
        Delete a collection by its ID.

        Args:
            collection_id (uuid.UUID): The UUID of the collection to delete
            organization_id (UUID): ID of the organization

        Returns:
            None
        """
        collection = (
            self.session.query(CollectionModel)
            .filter(
                CollectionModel.id==collection_id,
                CollectionModel.organization_id==organization_id
            )
            .first()
        )
        if collection:
            self.session.delete(collection)
            self.session.commit()

    def update(
        self,
        collection_id: UUID,
        data: CollectionUpdateDTO,
        organization_id: UUID
    ) -> Optional[Collection]:
        """
        Update a collection by its ID.

        Args:
            collection_id (UUID): The UUID of the collection to update.
            data (CollectionUpdateDTO): The data to update the collection with.
                Fields include:
                    - name (str)
            organization_id (UUID): ID of the organization

        Returns:
            Optional[Collection]: The updated collection object, or None if not found.
        """
        collection = (
            self.session.query(CollectionModel)
            .filter(
                CollectionModel.id==collection_id,
                CollectionModel.organization_id==organization_id
            )
            .first()
        )

        if not collection:
            return None

        update_data = data.model_dump(exclude_unset=True, exclude_none=True)
        for key, value in update_data.items():
            setattr(collection, key, value)

        self.session.commit()
        self.session.refresh(collection)

        return Collection.model_validate(collection)

    def exists(
        self,
        collection_id: UUID,
        organization_id: UUID
    ) -> bool:
        """
        Check if an collection with the given ID exists in the organization.

        Args:
            collection_id (UUID): The ID to check
            organization_id (UUID): ID of the organization

        Returns:
            bool: True if exists, False otherwise
        """
        return (
            self.session.query(
                self.session.query(CollectionModel)
                .filter(
                    CollectionModel.id == collection_id,
                    CollectionModel.organization_id == organization_id
                )
                .exists()
            )
            .scalar()
        )
