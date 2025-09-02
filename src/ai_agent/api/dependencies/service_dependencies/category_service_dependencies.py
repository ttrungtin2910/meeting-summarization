"""
Dependency injection module for Category-related services.
"""

from fastapi import Depends

from ai_agent.api.dependencies.repository_dependencies import (
    get_category_repository, get_collection_repository,
    get_document_repository, get_organization_repository)
from ai_agent.application.services.database_services import CategoryService
from ai_agent.infrastructure.database.repositories import (
    BaseCategoryRepository, BaseCollectionRepository, BaseDocumentRepository,
    BaseOrganizationRepository)


def get_category_service(
        category_repository: BaseCategoryRepository = Depends(get_category_repository),
        collection_repository: BaseCollectionRepository = Depends(get_collection_repository),
        document_repository: BaseDocumentRepository = Depends(get_document_repository),
        organization_repository: BaseOrganizationRepository = Depends(get_organization_repository)
) -> CategoryService:
    """
    Provides a CategoryService instance, with injected repositories.

    Args:
        category_repository (BaseCategoryRepository): An implementation of the
            BaseCategoryRepository interface used for data access operations.
        collection_repository (BaseCollectionRepository):
            repository for collection table
        document_repository (BaseDocumentRepository):
            repository for document table
        organization_repository (BaseOrganizationRepository):
            repository for organization table
    Returns:
        CategoryService: Service instance for category operations
    """
    return CategoryService(
        category_repository,
        collection_repository,
        document_repository,
        organization_repository
    )
