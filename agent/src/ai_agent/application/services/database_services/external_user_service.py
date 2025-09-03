"""
Service class for managing external users.
"""

from typing import List
from uuid import UUID

from ai_agent.domain.exceptions.external_user_exceptions import \
    ExternalUserNotFound
from ai_agent.domain.models.database_entities.external_user import ExternalUser
from ai_agent.domain.models.security_contexts.organization_context import \
    OrganizationContext
from ai_agent.infrastructure.database.repositories import \
    BaseExternalUserRepository


class ExternalUserService:
    """
    ExternalUserService provides logic to manage external users for a given client.
    """

    def __init__(
            self,
            external_user_repository: BaseExternalUserRepository
        ):
        self.external_user_repository = external_user_repository

    def get_external_user(
        self,
        external_user_id: UUID,
        organization_context: OrganizationContext,
    ) -> ExternalUser:
        """
        Retrieve a specific external user by ID for the current organization.

        Args:
            external_user_id (UUID): External user ID from the organization.
            organization_context (OrganizationContext): the authenticated organization.

        Returns:
            ExternalUser: The external user entity if found.

        Raises:
            ExternalUserNotFound: If the user does not exist.
        """
        organization_id = organization_context.organization_id
        result = self.external_user_repository.get_by_id(
            external_user_id=external_user_id,
            organization_id=organization_id,
        )
        if not result:
            raise ExternalUserNotFound()
        return result

    def list_external_users(
        self,
        organization_context: OrganizationContext ,
    ) -> List[ExternalUser]:
        """
        List all external users belonging to the current organization.

        Args:
            organization_context (OrganizationContext): the authenticated organization.

        Returns:
            List[ExternalUser]: List of external users.
        """
        organization_id = organization_context.organization_id
        return self.external_user_repository.list_external_users(
            organization_id=organization_id
        )

    def delete_external_user(
        self,
        external_user_id: UUID,
        organization_context: OrganizationContext ,
    ) -> None:
        """
        Delete an external user by ID for the current organization.

        Args:
            external_user_id (UUID): External user ID from the organization.
            organization_context (OrganizationContext): the authenticated organization.
        """
        organization_id = organization_context.organization_id
        current_external_user = self.external_user_repository.get_by_id(
            external_user_id=external_user_id,
            organization_id=organization_id
        )
        if not current_external_user:
            raise ExternalUserNotFound()

        self.external_user_repository.delete(
            external_user_id=external_user_id,
            organization_id=organization_id
        )
