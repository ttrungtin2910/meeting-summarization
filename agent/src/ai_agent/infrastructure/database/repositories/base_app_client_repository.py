"""
Defines the abstract base repository interface for working with AppClient entities.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from ai_agent.domain.dtos.app_client_dto import (AppClientCreateDTO,
                                                 AppClientUpdateDTO)
from ai_agent.domain.models.database_entities.app_client import AppClient


class BaseAppClientRepository(ABC):
    """
    Abstract base class for AppClient repository.
    """

    @abstractmethod
    def get_by_client_id(
        self,
        client_id: UUID,
    ) -> Optional[AppClient]:
        """
        Retrieve a single AppClient by client_id, scoped to a specific organization.

        Parameters:
            client_id (UUID): The unique identifier of the AppClient to retrieve.

        Returns:
            Optional[AppClient]: The AppClient object if found, otherwise None.
        """

    @abstractmethod
    def get_by_name(
        self,
        name: str,
        organization_id: UUID
    ) -> Optional[AppClient]:
        """
        Retrieve an AppClient by name within a specific organization.

        Parameters:
            name (str): The name of the AppClient.
            organization_id (UUID): The organization the client belongs to.

        Returns:
            Optional[AppClient]: The AppClient object if found, otherwise None.
        """

    @abstractmethod
    def exists(self, name: str, organization_id: UUID) -> bool:
        """
        Check if an AppClient with the given name already exists in the organization.

        Parameters:
            name (str): The name of the AppClient to check.
            organization_id (UUID): The organization in which to check.

        Returns:
            bool: True if an AppClient with the given name exists, False otherwise.
        """

    @abstractmethod
    def list_by_organization(self, organization_id: UUID) -> List[AppClient]:
        """
        Retrieve all AppClients for a given organization.

        Parameters:
            organization_id (UUID): The unique identifier of the organization.

        Returns:
            List[AppClient]: A list of AppClient objects associated with the organization.
        """

    @abstractmethod
    def create(
        self,
        data: AppClientCreateDTO,
        organization_id: UUID
    ) -> AppClient:
        """
        Create a new AppClient under the specified organization.

        Parameters:
            data (AppClientCreateDTO): The data transfer object
                containing the details for the new AppClient.
            organization_id (UUID): The unique identifier of the organization
                under which the AppClient is created.

        Returns:
            AppClient: The newly created AppClient entity.
        """

    @abstractmethod
    def update(
        self,
        client_id: UUID,
        organization_id: UUID,
        data: AppClientUpdateDTO
    ) -> Optional[AppClient]:
        """
        Update an AppClient within the specified organization.

        Parameters:
            client_id (UUID): The unique identifier of the AppClient to update.
            organization_id (UUID): The unique identifier of the organization
                to which the AppClient belongs.
            data (AppClientUpdateDTO): The data transfer object
                containing the updated details for the AppClient.

        Returns:
            Optional[AppClient]: The updated AppClient object
                if found within the specified organization, otherwise None.
        """

    @abstractmethod
    def delete(self, client_id: UUID, organization_id: UUID) -> None:
        """
        Delete an AppClient if it belongs to the specified organization.

        Parameters:
            client_id (UUID): The unique identifier of the AppClient to delete.
            organization_id (UUID): The unique identifier of the organization
                to which the AppClient belongs.

        Returns:
            None
        """
