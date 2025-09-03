"""
Dependency injection module for Authentication services.
"""

from fastapi import Depends

from ai_agent.api.dependencies.password_hasher_dependencies import \
    get_password_hasher
from ai_agent.api.dependencies.repository_dependencies import (
    get_admin_repository, get_app_client_repository,
    get_organization_repository)
from ai_agent.api.dependencies.token_manager_dependencies import \
    get_token_manager
from ai_agent.application.services.auth_service import AuthService
from ai_agent.infrastructure.database.repositories import (
    BaseAdminRepository, BaseAppClientRepository, BaseOrganizationRepository)
from ai_agent.infrastructure.password_hasher.base_password_hasher import \
    BasePasswordHasher
from ai_agent.infrastructure.token_manager.base_token_manager import \
    BaseTokenManager


def get_auth_service(
        admin_repository: BaseAdminRepository = Depends(get_admin_repository),
        organization_repository: BaseOrganizationRepository = Depends(get_organization_repository),
        app_client_repository: BaseAppClientRepository = Depends(get_app_client_repository),
        token_manager: BaseTokenManager = Depends(get_token_manager),
        password_hasher: BasePasswordHasher = Depends(get_password_hasher)
) -> AuthService:
    """
    Provides AuthService with injected dependencies.

    Args:
        admin_repository (BaseAdminRepository): Repository to access admin info.
        app_client_repository (BaseAppClientRepository): Repository to access app client info.
        token_manager (BaseTokenManager): manager to generate and verify JWT tokens.
        organization_repository (BaseOrganizationRepository):
            Repository to access organization table.
        password_hasher (BasePasswordHasher): Service to hash and verify passwords.

    Returns:
        AuthService: Instance of AuthService with dependencies injected.
    """
    return AuthService(
        admin_repository=admin_repository,
        organization_repository=organization_repository,
        app_client_repository=app_client_repository,
        token_manager=token_manager,
        password_hasher=password_hasher,
    )
