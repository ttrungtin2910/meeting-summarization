"""
Repository for Collection model.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from ai_agent.domain.dtos.collection_dto import (CollectionCreateDTO,
                                                 CollectionUpdateDTO)
from ai_agent.domain.models.database_entities.collection import Collection


class BaseCollectionRepository(ABC):
    """
    Abstract base repository class for managing Collection model operations.

    This abstract class defines the interface for Collection repositories,
    """

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
    def exists(
        self,
        collection_id: UUID,
        organization_id: UUID
    ) -> bool:
        """
        Check if an collection with the given ID exists.

        Args:
            collection_id (UUID): The ID to check
            organization_id (UUID): ID of the organization

        Returns:
            bool: True if exists, False otherwise
        """
