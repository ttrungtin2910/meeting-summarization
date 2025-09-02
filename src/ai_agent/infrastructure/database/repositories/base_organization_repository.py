"""
Organization repository interface module.

This module defines the abstract base class for organization repositories
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from ai_agent.domain.dtos.organization_dto import (OrganizationCreateDTO,
                                                   OrganizationUpdateDTO)
from ai_agent.domain.models.database_entities.organization import Organization


class BaseOrganizationRepository(ABC):
    """
    Abstract base class for organization data access operations.

    This interface defines the contract for repository implementations
    that handle persistence operations for organization entities.
    All concrete repositories must implement these methods.

    Methods are defined for the standard CRUD operations:
    create, read (get_list), update, and delete.
    """

    @abstractmethod
    def create(self, data: OrganizationCreateDTO) -> Organization:
        """
        Create a new organization.

        Args:
            data (OrganizationCreateDTO): Data transfer object containing
                                         organization creation data

        Returns:
            Organization: The newly created organization domain entity
        """

    @abstractmethod
    def get_by_id(self, organization_id: UUID) -> Optional[Organization]:
        """
        Retrieve a organization by its ID.

        Args:
            organization_id (UUID): The UUID of the organization to retrieve

        Returns:
            Optional[Organization]: The organization if found, None otherwise
        """

    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Organization]:
        """
        Retrieve an organization by its name.

        Args:
        name (str): The name of the organization to retrieve

        Returns:
        Organization: The organization domain entity, or None if does not exist

        Raises:
        OrganizationNotFound: If no organization with the given name is found
        """

    @abstractmethod
    def get_list(self) -> List[Organization]:
        """
        Retrieve all organizations.

        Returns:
            List[Organization]: A list of all organization domain entities
        """

    @abstractmethod
    def update(self, organization_id: UUID, data: OrganizationUpdateDTO) -> Organization:
        """
        Update an existing organization.

        Args:
            organization_id (UUID): The unique identifier of the organization to update
            data (OrganizationUpdateDTO): Data transfer object containing
                                        the fields to update

        Returns:
            Organization: The updated organization domain entity
        """

    @abstractmethod
    def delete(self, organization_id: UUID) -> None:
        """
        Delete an organization.

        Args:
            organization_id (UUID): The unique identifier of the organization to delete
        """

    @abstractmethod
    def exists(self, organization_id: UUID) -> bool:
        """
        Check if an organization with the given ID exists.

        Args:
            organization_id (UUID): The ID to check

        Returns:
            bool: True if exists, False otherwise
        """

    @abstractmethod
    def activate(self, organization_id: UUID) -> None:
        """
        Activate an organization.

        Args:
            organization_id (UUID):
                The unique identifier of the organization to activate
        """

    @abstractmethod
    def deactivate(self, organization_id: UUID) -> None:
        """
        Deactivate an organization.

        Args:
            organization_id (UUID):
                The unique identifier of the organization to deactivate
        """
