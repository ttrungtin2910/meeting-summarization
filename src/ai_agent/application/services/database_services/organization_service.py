"""
This module defines the OrganizationService class for managing organization operations.

The OrganizationService class provides business logic for creating, retrieving,
updating, and deleting organizations, acting as a bridge between the API and
repository layers.
"""

from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID

from ai_agent.domain.dtos.organization_dto import (
    OrganizationCreateDTO, OrganizationCreateRequestDTO, OrganizationUpdateDTO,
    OrganizationUpdateRequestDTO)
from ai_agent.domain.exceptions.organization_exceptions import (
    OrganizationAlreadyExists, OrganizationInUse, OrganizationNotFound)
from ai_agent.domain.models.database_entities.organization import Organization
from ai_agent.infrastructure.database.repositories import \
    BaseOrganizationRepository, BaseCollectionRepository
from ai_agent.infrastructure.password_hasher.base_password_hasher import \
    BasePasswordHasher


class OrganizationService:
    """
    Service for managing organization operations.

    This service class provides business logic for organization-related operations
    such as creation, retrieval, and management, serving as an intermediary between
    the API layer and the repository layer.
    """
    def __init__(
            self,
            organization_repository: BaseOrganizationRepository,
            collection_repository: BaseCollectionRepository,
            password_hasher: BasePasswordHasher
        ):
        """
        Initialize the organization service with a repository.

        Args:
            organization_repository (BaseOrganizationRepository):
                Repository for organization data access
            collection_repository (BaseCollectionRepository):
                Repository for collection data access
            password_hasher (BasePasswordHasher):
                Password hashing service for securing passwords
        """
        self.organization_repository = organization_repository
        self.collection_repository = collection_repository
        self.password_hasher = password_hasher

    def create_organization(
            self,
            data: OrganizationCreateRequestDTO,
        ) -> Organization:
        """
        Create a new organization.

        Args:
            data (OrganizationCreateRequestDTO): Data transfer object with organization details

        Returns:
            Organization: The newly created organization object

        Raises:
            OrganizationAlreadyExists: If an organization with the given name already exists
            ValueError: If organization name is empty
        """
        organization_name = data.name.strip()
        if not organization_name:
            raise ValueError("Organization name cannot be empty")

        database_organization = self.organization_repository.get_by_name(organization_name)

        if database_organization:
            raise OrganizationAlreadyExists(organization_name=organization_name)

        # Hash the password
        hashed_password = self.password_hasher.hash(data.password)

        # Create DTO
        organization_dto = OrganizationCreateDTO(
            name=data.name,
            hashed_password=hashed_password,
            created_at=datetime.now(tz=timezone.utc),
        )

        new_organization = self.organization_repository.create(organization_dto)
        return new_organization

    def get_organization(
            self,
            organization_id: UUID,
        ) -> Organization:
        """
        Get an organization.

        Args:
            organization_id (UUID)

        Returns:
            Organization

        Raises:
            OrganizationNotFound: If the organization with the given ID does not exist
        """
        organization = self.organization_repository.get_by_id(organization_id)
        if not organization:
            raise OrganizationNotFound
        return organization

    def get_list_organizations(
            self,
        ) -> List[Organization]:
        """
        Get list of all organizations.

        Returns:
            List[Organization]
        """
        organizations = self.organization_repository.get_list()
        return organizations

    def update_organization(
            self,
            organization_id: UUID,
            data: OrganizationUpdateRequestDTO,
        ) -> Organization:
        """
        Update an existing organization.

        Args:
            organization_id (UUID): ID of the organization that needs to update
            data (OrganizationUpdateRequestDTO): DTO containing the updated organization information

        Returns:
            Organization: The updated organization object

        Raises:
            OrganizationNotFound: If the organization with the given ID does not exist
        """
        organization: Optional[Organization] = self.organization_repository.get_by_id(
            organization_id
        )
        if not organization:
            raise OrganizationNotFound


        # Check if no field changed compared to the existed organization
        has_changed = False
        update_data = data.model_dump(exclude_unset=True, exclude_none=True, exclude={"password"})

        # if change password
        if data.password:
            hashed_password = self.password_hasher.hash(data.password)
            update_data['hashed_password'] = hashed_password
        else:
            update_data['hashed_password'] = organization.hashed_password

        for field, new_value in update_data.items():
            old_value = getattr(organization, field, None)
            if new_value != old_value:
                has_changed = True
                break

        # If no change, return the original organization
        if not has_changed:
            return organization

        # If has change
        update_dto = OrganizationUpdateDTO(**update_data)
        updated_organization = self.organization_repository.update(organization_id, update_dto)
        assert updated_organization is not None
        return updated_organization

    def delete_organization(
            self,
            organization_id: UUID,
        ) -> None:
        """
        Delete an organization.

        Args:
            organization_id (UUID)

        Returns:
            None

        Raises:
            OrganizationNotFound: If the organization with the given ID does not exist
        """
        # Check if organization exists
        organization = self.organization_repository.get_by_id(organization_id)
        if not organization:
            raise OrganizationNotFound

        # Check if exist collections belong to the organization
        collections = self.collection_repository.get_list(
            organization_id=organization_id
        )
        if collections:
            raise OrganizationInUse(
                organization_id=organization_id
            )
        self.organization_repository.delete(organization_id)

    def activate(
            self,
            organization_id: UUID
        ) -> None:
        """
        Activate an organization.

        Args:
            organization_id (UUID): The ID of the organization to be activated.

        Returns:
            None

        Raises:
            OrganizationNotFound: If the organization with the given ID does not exist.
        """
        # Check if organization exists
        organization = self.organization_repository.get_by_id(organization_id)
        if not organization:
            raise OrganizationNotFound

        # Activate
        self.organization_repository.activate(
            organization_id=organization_id
        )

    def deactivate(
            self,
            organization_id: UUID
        ) -> None:
        """
        Deactivate an organization.

        Args:
            organization_id (UUID): The ID of the organization to be deactivated.

        Returns:
            None

        Raises:
            OrganizationNotFound: If the organization with the given ID does not exist.
        """
        # Check if organization exists
        organization = self.organization_repository.get_by_id(organization_id)
        if not organization:
            raise OrganizationNotFound

        # Activate
        self.organization_repository.deactivate(
            organization_id=organization_id
        )
