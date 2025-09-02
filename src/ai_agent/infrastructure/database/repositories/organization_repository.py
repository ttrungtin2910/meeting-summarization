"""
Implementation of the organization repository.
"""

from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from ai_agent.domain.dtos.organization_dto import (OrganizationCreateDTO,
                                                   OrganizationUpdateDTO)
from ai_agent.domain.exceptions.organization_exceptions import \
    OrganizationNotFound
from ai_agent.domain.models.database_entities.organization import Organization
from ai_agent.infrastructure.database.models.organization_model import \
    OrganizationModel

from .base_organization_repository import BaseOrganizationRepository


class OrganizationRepository(BaseOrganizationRepository):
    """
    The implementation of the organization repository.
    """

    def __init__(self, session: Session):
        """
        Initialize the repository with a database session.

        Args:
            session (Session): database session for database operations
        """
        self.session = session

    def create(self, data: OrganizationCreateDTO) -> Organization:
        """
        Create a new organization in the database.

        Args:
            data (OrganizationCreateDTO): Data transfer object with organization details

        Returns:
            Organization: The newly created organization domain entity
        """
        organization = OrganizationModel(**data.model_dump())
        self.session.add(organization)
        self.session.commit()
        self.session.refresh(organization)
        return Organization.model_validate(organization)

    def get_by_id(self, organization_id: UUID) -> Optional[Organization]:
        """
        Retrieve a organization by its ID.

        Args:
            organization_id (UUID): The UUID of the organization to retrieve

        Returns:
            Optional[Organization]: The organization if found, None otherwise
        """
        organization = (
            self.session.query(OrganizationModel)
            .filter(OrganizationModel.id == organization_id)
            .first()
        )
        if organization is None:
            return None
        return Organization.model_validate(organization)

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
        organization = self.session.query(OrganizationModel).filter_by(name=name).first()
        if not organization:
            return None
        return Organization.model_validate(organization)

    def get_list(self) -> list[Organization]:
        """
        Retrieve all organizations from the database.

        Returns:
            list[Organization]: A list of all organization domain entities
        """
        results = self.session.query(OrganizationModel).all()
        return [Organization.model_validate(result) for result in results]

    def update(self, organization_id: UUID, data: OrganizationUpdateDTO) -> Organization:
        """
        Update an existing organization in the database.

        Args:
            organization_id (UUID): The unique identifier of the organization to update
            data (OrganizationUpdateDTO): Data transfer object with updated fields

        Returns:
            Organization: The updated organization domain entity

        Raises:
            ValueError: If the organization with the specified ID is not found
        """
        organization = self.session.get(OrganizationModel, organization_id)
        if not organization:
            raise OrganizationNotFound

        update_data = data.model_dump(exclude_unset=True, exclude_none=True)
        for key, value in update_data.items():
            setattr(organization, key, value)

        self.session.commit()
        self.session.refresh(organization)
        return Organization.model_validate(organization)

    def delete(self, organization_id: UUID) -> None:
        """
        Delete an organization from the database.

        Args:
            organization_id (UUID): The unique identifier of the organization to delete

        Raises:
            ValueError: If the organization with the specified ID is not found
        """
        organization = self.session.get(OrganizationModel, organization_id)

        if not organization:
            raise OrganizationNotFound

        self.session.delete(organization)
        self.session.commit()

    def exists(self, organization_id: UUID) -> bool:
        """
        Check if an organization with the given ID exists.

        Args:
            organization_id (UUID): The ID to check

        Returns:
            bool: True if exists, False otherwise
        """
        return (
            self.session.query(
                self.session.query(OrganizationModel)
                .filter(OrganizationModel.id == organization_id)
                .exists()
            )
            .scalar()
        )

    def activate(self, organization_id: UUID) -> None:
        """
        Activate an organization.

        Args:
            organization_id (UUID):
                The unique identifier of the organization to activate
        """
        statement = (
            select(OrganizationModel)
            .where(
                OrganizationModel.id == organization_id
            )
        )
        organization = self.session.execute(statement).scalar_one_or_none()
        if organization:
            organization.is_active = True
            self.session.commit()

    def deactivate(self, organization_id: UUID) -> None:
        """
        Deactivate an organization.

        Args:
            organization_id (UUID):
                The unique identifier of the organization to deactivate
        """
        statement = (
            select(OrganizationModel)
            .where(
                OrganizationModel.id == organization_id
            )
        )
        organization = self.session.execute(statement).scalar_one_or_none()
        if organization:
            organization.is_active = False
            self.session.commit()
