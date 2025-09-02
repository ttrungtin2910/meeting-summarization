"""
Dependency injection module for App Client Service.
"""

from fastapi import Depends

from ai_agent.api.dependencies.repository_dependencies import (
    get_app_client_repository, get_collection_repository,
    get_organization_repository)
from ai_agent.application.services.database_services import AppClientService
from ai_agent.infrastructure.database.repositories import (
    BaseAppClientRepository, BaseCollectionRepository,
    BaseOrganizationRepository)


def get_app_client_service(
    app_client_repository: BaseAppClientRepository = Depends(get_app_client_repository),
    organization_repository: BaseOrganizationRepository = Depends(get_organization_repository),
    collection_repository: BaseCollectionRepository = Depends(get_collection_repository)
) -> AppClientService:
    """
    Provides an AppClientService instance with injected dependencies.

    Args:
        app_client_repository (BaseAppClientRepository): For accessing AppClient table.
        organization_repository (BaseOrganizationRepository): For validating organization.
        collection_repository (BaseCollectionRepository): For validating collection.

    Returns:
        AppClientService: Service to manage app clients.
    """
    return AppClientService(
        app_client_repository=app_client_repository,
        organization_repository=organization_repository,
        collection_repository=collection_repository
    )
