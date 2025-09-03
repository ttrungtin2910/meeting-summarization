"""
Provides dependency injection for EmbeddingService.

This module defines a FastAPI dependency to inject all required repositories
into the EmbeddingService for managing vector embeddings.
"""

from fastapi import Depends

from ai_agent.api.dependencies.repository_dependencies import (
    get_category_repository, get_collection_repository,
    get_document_repository, get_embedding_repository,
    get_organization_repository)
from ai_agent.application.services.database_services import EmbeddingService
from ai_agent.infrastructure.database.repositories import (
    BaseCategoryRepository, BaseCollectionRepository, BaseDocumentRepository,
    BaseEmbeddingRepository, BaseOrganizationRepository)


def get_embedding_service(
    collection_repository: BaseCollectionRepository = Depends(
        get_collection_repository
    ),
    category_repository: BaseCategoryRepository = Depends(
        get_category_repository
    ),
    document_repository: BaseDocumentRepository = Depends(
        get_document_repository
    ),
    embedding_repository: BaseEmbeddingRepository = Depends(
        get_embedding_repository
    ),
    organization_repository: BaseOrganizationRepository = Depends(
        get_organization_repository
    )
) -> EmbeddingService:
    """
    Provides an instance of EmbeddingService with injected repositories.

    Args:
        collection_repository (BaseCollectionRepository): Handles collection data.
        category_repository (BaseCategoryRepository): Handles category data.
        document_repository (BaseDocumentRepository): Handles document data.
        embedding_repository (BaseEmbeddingRepository): Handles embedding data.
        organization_repository (BaseOrganizationRepository):
            repository for organization table

    Returns:
        EmbeddingService: A fully initialized embedding service.
    """
    return EmbeddingService(
        collection_repository=collection_repository,
        category_repository=category_repository,
        document_repository=document_repository,
        embedding_repository=embedding_repository,
        organization_repository=organization_repository
    )
