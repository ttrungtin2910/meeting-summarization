"""
This module defines the AuthService class,
which handles client authentication and JWT generation.
"""

from typing import Optional
from uuid import UUID

from ai_agent.domain.exceptions.auth_exceptions import InvalidCredentials
from ai_agent.domain.models.database_entities.admin import Admin
from ai_agent.domain.models.database_entities.app_client import AppClient
from ai_agent.domain.models.database_entities.organization import Organization
from ai_agent.infrastructure.database.repositories import (
    BaseAdminRepository, BaseAppClientRepository, BaseOrganizationRepository)
from ai_agent.infrastructure.password_hasher.base_password_hasher import \
    BasePasswordHasher
from ai_agent.infrastructure.token_manager.base_token_manager import \
    BaseTokenManager


class AuthService:
    """
    AuthService provides authentication services and token generation for application clients.
    """
    def __init__(
            self,
            admin_repository: BaseAdminRepository,
            organization_repository: BaseOrganizationRepository,
            app_client_repository: BaseAppClientRepository,
            token_manager: BaseTokenManager,
            password_hasher: BasePasswordHasher,
        ):
        """
        Initializes the AuthService

        Args:
            admin_repository (BaseAdminRepository):
                An instance of BaseAdminRepository for data access.
            organization_repository (BaseOrganizationRepository):
                An instance for organization data access.
            app_client_repository (BaseAppClientRepository):
                An instance of BaseAppClientRepository for client data access.
            token_manager (BaseTokenManager): manager for token creation and verification.
            password_hasher (BasePasswordHasher):
        """
        self.admin_repository = admin_repository
        self.organization_repository = organization_repository
        self.app_client_repository = app_client_repository
        self.token_manager = token_manager
        self.password_hasher = password_hasher

    def login_client(
            self,
            client_id: UUID,
            client_secret: str,
        ) -> str:
        """
        Authenticates a client using their ID and secret, and generates a JWT if successful.

        Args:
            client_id: A UUID representing the unique identifier of the client.
            client_secret: A string representing the secret key of the client.

        Returns:
            A string representing the generated JWT.

        Raises:
            InvalidCredentials: If the client ID is not found
                or the client secret is incorrect.
        """
        # Retrieve the client using the provided client_id
        client: Optional[AppClient] = self.app_client_repository.get_by_client_id(
            client_id=client_id
        )

        # Check credentials
        if (
            not client or
            client.client_secret != client_secret or
            client.is_active is False
        ):
            raise InvalidCredentials()

        # Prepare the payload for the JWT
        payload = {
            "client_id": str(client_id),
            "organization_id": str(client.organization_id),
            "collection_ids": [str(collection_id) for collection_id in client.collection_ids]
        }

        # Create and return the JWT
        token = self.token_manager.encode(payload)
        return token

    def login_organization(self, name: str, password: str) -> str:
        """
        Authenticate an organization based on name and password.

        Args:
            name (str): The name of the organization attempting to login.
            password (str): The plain text password.

        Returns:
            A string representing the generated JWT.
        """
        organization: Organization | None = self.organization_repository.get_by_name(name)
        if not organization:
            raise InvalidCredentials()

        if not self.password_hasher.verify(password, organization.hashed_password):
            raise InvalidCredentials()

        payload = {
            "organization_id": str(organization.id),
        }

        # Create and return the JWT
        token = self.token_manager.encode(payload)
        return token

    def login_admin(self, email: str, password: str) -> str:
        """
        Authenticate an admin based on email and password.

        Args:
            email (str): The email of the admin attempting to login.
            password (str): The plain text password.

        Returns:
            A string representing the generated JWT.
        """
        admin: Optional[Admin] = self.admin_repository.get_by_email(email)
        if not admin:
            raise InvalidCredentials

        if not self.password_hasher.verify(password, admin.hashed_password):
            raise InvalidCredentials

        payload = {
            "admin_id": str(admin.id),
        }

        # Create and return the JWT
        token = self.token_manager.encode(payload)
        return token
