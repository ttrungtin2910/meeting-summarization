"""
Dependency injection module for Document-related services.
"""

from fastapi import Depends

from ai_agent.api.dependencies.repository_dependencies import (
    get_category_repository, get_collection_repository,
    get_document_repository, get_organization_repository)
from ai_agent.application.services.database_services import DocumentService
from ai_agent.config import StorageConfig
from ai_agent.infrastructure.database.repositories import (
    BaseCategoryRepository, BaseCollectionRepository, BaseDocumentRepository,
    BaseOrganizationRepository)
from ai_agent.infrastructure.storage.factory import get_storage


def get_expire_minutes():
    """
    Get the configured expiration time for download URLs.

    This function retrieves the expiration time in minutes for download URLs
    from the application configuration.

    Returns:
        int: The number of minutes before download URLs expire
    """
    return StorageConfig.expire_minutes


def get_document_service(
        collection_repository: BaseCollectionRepository = Depends(
            get_collection_repository
        ),
        category_repository: BaseCategoryRepository = Depends(
            get_category_repository
        ),
        document_repository: BaseDocumentRepository = Depends(
            get_document_repository
        ),
        organization_repository: BaseOrganizationRepository = Depends(
            get_organization_repository
        ),
        storage = Depends(get_storage),
        expire_minutes: int = Depends(get_expire_minutes)
    ) -> DocumentService:
    """
    Provides a DocumentService instance, with injected repositories.

    Args:
        collection_repository (BaseCollectionRepository):
            Collection Repository to work with collections table
        category_repository (BaseCategoryRepository):
            Category Repository to work with categories table
        document_repository (BaseDocumentRepository):
            Document Repository to work with documents table
        organization_repository (BaseOrganizationRepository):
            repository for organization table
        storage (BaseStorage):  Storage service instance to save or download file
        expire_minutes (int):
            The number of minutes for which the uploaded file will be available for download

    Returns:
        DocumentService: Service instance for document operations
    """
    return DocumentService(
        collection_repository,
        category_repository,
        document_repository,
        organization_repository,
        storage,
        expire_minutes
    )
