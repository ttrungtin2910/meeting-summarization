"""
This module provides a concrete implementation of BaseExternalUserRepository,
using SQLAlchemy ORM for performing CRUD operations on ExternalUser entities.
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import and_, delete, select
from sqlalchemy.orm import Session

from ai_agent.domain.models.database_entities.external_user import ExternalUser
from ai_agent.infrastructure.database.models.external_user_model import \
    ExternalUserModel
from ai_agent.infrastructure.database.repositories import \
    BaseExternalUserRepository


class ExternalUserRepository(BaseExternalUserRepository):
    """
    Repository class for ExternalUser model.
    """

    def __init__(self, session: Session):
        """
        Initialize the ExternalUserRepository with a database session.

        Args:
            session (Session): SQLAlchemy database session.
        """
        self.session = session

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
        model = ExternalUserModel(
            external_user=external_user,
            organization_id=organization_id,
            client_id=client_id
        )
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return ExternalUser.model_validate(model)

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
        statement = (
            select(ExternalUserModel)
            .where(
                and_(
                    ExternalUserModel.id == external_user_id,
                    ExternalUserModel.organization_id == organization_id,
                )
            )
        )
        result = self.session.execute(statement).scalar_one_or_none()
        return ExternalUser.model_validate(result) if result else None

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
        statement = (
            select(ExternalUserModel)
            .where(
                and_(
                    ExternalUserModel.external_user == external_user,
                    ExternalUserModel.organization_id == organization_id,
                    ExternalUserModel.client_id == client_id
                )
            )
        )
        result = self.session.execute(statement).scalar_one_or_none()
        return ExternalUser.model_validate(result) if result else None

    def list_external_users(
        self,
        organization_id: UUID,
    ) -> List[ExternalUser]:
        """
        List all external users for a given client and organization.

        Args:
            organization_id (UUID): Organization ID.

        Returns:
            List[ExternalUser]: A list of matching external users.
        """
        statement = select(ExternalUserModel).where(
            ExternalUserModel.organization_id == organization_id,
        )
        results = self.session.execute(statement).scalars().all()
        return [ExternalUser.model_validate(r) for r in results]

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
        statement = (
            delete(ExternalUserModel)
            .where(
                and_(
                    ExternalUserModel.id == external_user_id,
                    ExternalUserModel.organization_id == organization_id,
                )
            )
        )
        self.session.execute(statement)
        self.session.commit()
