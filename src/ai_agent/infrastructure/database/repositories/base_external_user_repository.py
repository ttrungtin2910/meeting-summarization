"""
Defines the abstract base repository interface for working with
ExternalUser entities.

ExternalUser represents a user from an external system,
identified by an external_user
and associated with a specific app client and organization.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from ai_agent.domain.models.database_entities.external_user import ExternalUser


class BaseExternalUserRepository(ABC):
    """
    Abstract base class for ExternalUser repository.
    """

    @abstractmethod
    def create(
        self,
        external_user: str,
        organization_id: UUID,
        client_id: UUID
    ) -> ExternalUser:
        """
        Create a new external user.

        Parameters:
            external_user (str): The ID of the external user from the client system.
            organization_id (UUID): The organization to which this user belongs.
            client_id (UUID): ID of the app client

        Returns:
            ExternalUser: The newly created ExternalUser entity.
        """

    @abstractmethod
    def get_by_id(
        self,
        external_user_id: UUID,
        organization_id: UUID,
    ) -> Optional[ExternalUser]:
        """
        Retrieve an external user by external_user_id, and organization_id.

        Parameters:
            external_user_id (UUID): The ID from the external system.
            organization_id (UUID): The organization to which this user belongs.

        Returns:
            Optional[ExternalUser]: The matching ExternalUser object, if found.
        """

    @abstractmethod
    def get_by_external_user(
        self,
        external_user: str,
        organization_id: UUID,
        client_id: UUID
    ) -> Optional[ExternalUser]:
        """
        Retrieve a specific external user.

        Args:
            external_user (str): External user ID.
            organization_id (UUID): Organization ID.
            client_id (UUID): ID of the app client

        Returns:
            Optional[ExternalUser]: The ExternalUser object if found.
        """

    @abstractmethod
    def list_external_users(
        self,
        organization_id: UUID,
    ) -> List[ExternalUser]:
        """
        List all external users belonging to a given client and organization.

        Parameters:
            organization_id (UUID): The organization to filter users by.

        Returns:
            List[ExternalUser]: A list of ExternalUser objects.
        """

    @abstractmethod
    def delete(
        self,
        external_user_id: UUID,
        organization_id: UUID,
    ) -> None:
        """
        Delete an external user by external_user, client_id, and organization_id.

        Parameters:
            external_user_id (UUID): The external user ID from the organization.
            organization_id (UUID): The organization to which this user belongs.

        Returns:
            None
        """
