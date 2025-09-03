"""
Dependency injection module for external user-related services.
"""

from fastapi import Depends

from ai_agent.api.dependencies.repository_dependencies import \
    get_external_user_repository
from ai_agent.application.services.database_services import ExternalUserService
from ai_agent.infrastructure.database.repositories import \
    BaseExternalUserRepository


def get_external_user_service(
    external_user_repository: BaseExternalUserRepository = Depends(
        get_external_user_repository
    ),
) -> ExternalUserService:
    """
    Factory function that provides a configured ExternalUserService instance.

    Args:
        external_user_repository (BaseExternalUserRepository):
            The repository implementation for external users.

    Returns:
        ExternalUserService: A configured external user service.
    """
    return ExternalUserService(external_user_repository=external_user_repository)
