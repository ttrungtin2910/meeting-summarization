"""
Provides dependency injection for DocumentSyncService.
"""

from fastapi import Depends

from ai_agent.api.dependencies.repository_dependencies import (
    get_collection_repository, get_document_repository,
    get_embedding_repository, get_organization_repository)
from ai_agent.application.services.sync_services.document_sync_service import \
    DocumentSyncService
from ai_agent.infrastructure.database.repositories import (
    BaseCollectionRepository, BaseDocumentRepository, BaseEmbeddingRepository,
    BaseOrganizationRepository)
from ai_agent.infrastructure.document_embedder.base import BaseEmbedder
from ai_agent.infrastructure.document_embedder.factory import get_embedder
from ai_agent.infrastructure.document_splitter.base import BaseSplitter
from ai_agent.infrastructure.document_splitter.factory import get_splitter
from ai_agent.infrastructure.storage.base import BaseStorage
from ai_agent.infrastructure.storage.factory import get_storage


def get_document_sync_service(
        document_repository: BaseDocumentRepository = Depends(
            get_document_repository
        ),
        embedding_repository: BaseEmbeddingRepository = Depends(
            get_embedding_repository
        ),
        collection_repository: BaseCollectionRepository = Depends(
            get_collection_repository
        ),
        organization_repository: BaseOrganizationRepository = Depends(
            get_organization_repository
        ),
        storage: BaseStorage = Depends(get_storage),
        splitter: BaseSplitter = Depends(get_splitter),
        embedder: BaseEmbedder = Depends(get_embedder),
) -> DocumentSyncService:
    """
    Creates and returns an instance of DocumentSyncService.

    Args:
        document_repository (BaseDocumentRepository):
            The repository for managing documents.
        embedding_repository (BaseEmbeddingRepository):
            The repository for managing embeddings.
        collection_repository (BaseCollectionRepository):
            The repository for managing collections.
        organization_repository (BaseOrganizationRepository):
            The repository for managing organizations.
        storage (BaseStorage): The storage service for handling document storage.
        splitter (BaseSplitter): The service for splitting documents into parts.
        embedder (BaseEmbedder): The service for embedding documents.

    Returns:
    - DocumentSyncService: An instance of DocumentSyncService
        configured with the provided dependencies.
    """
    return DocumentSyncService(
        document_repository=document_repository,
        embedding_repository=embedding_repository,
        collection_repository=collection_repository,
        organization_repository=organization_repository,
        storage=storage,
        splitter=splitter,
        embedder=embedder,
    )
