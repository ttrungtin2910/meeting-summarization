"""
Dependency injection module for Collection-related services
"""

from fastapi import Depends

from ai_agent.api.dependencies.repository_dependencies import (
    get_category_repository, get_collection_repository,
    get_organization_repository)
from ai_agent.application.services.database_services import CollectionService
from ai_agent.infrastructure.database.repositories import (
    BaseOrganizationRepository, CategoryRepository, CollectionRepository)


def get_collection_service(
    collection_repository: CollectionRepository = Depends(
        get_collection_repository
    ),
    category_repository: CategoryRepository = Depends(
        get_category_repository
    ),
    organization_repository: BaseOrganizationRepository = Depends(
        get_organization_repository
    )
) -> CollectionService:
    """
    Provides a CollectionService instance, with injected repository.

    Args:
        collection_repository (CollectionRepository):
            Repository to be used by the service
        category_repository (CategoryRepository):
            Repository for category data access
        organization_repository (BaseOrganizationRepository):
            repository for organization table

    Returns:
        CollectionService: Service instance for collection operations
    """
    return CollectionService(
        collection_repository,
        category_repository,
        organization_repository
    )
