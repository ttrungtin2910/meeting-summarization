"""
Dependency injection for retrievers.

This module provides factory functions for creating and configuring retriever objects
that can be injected as dependencies in FastAPI routes or other services.
"""

from ai_agent.application.services.embedding_query_service import \
    EmbeddingQueryService
from ai_agent.infrastructure.database.base.session import get_db
from ai_agent.infrastructure.database.repositories import (
    CollectionRepository, EmbeddingRepository)
from ai_agent.infrastructure.document_embedder.factory import get_embedder
from ai_agent.infrastructure.retrievers.embedding_retriever import \
    EmbeddingRetriever


def get_embedding_retriever() -> EmbeddingRetriever:
    """
    Create and return a configured EmbeddingRetriever instance.

    Sets up all necessary dependencies for the retriever including a database session,
    repository, embedder, and query service.

    Returns:
        EmbeddingRetriever: A configured retriever for finding similar embeddings
    """
    session = next(get_db())
    try:
        embedding_repository = EmbeddingRepository(session)
        collection_repository = CollectionRepository(session)
        embedder = get_embedder()

        embedding_query_service = EmbeddingQueryService(
            embedding_repository=embedding_repository,
            collection_repository=collection_repository,
            embedder=embedder
        )
        return EmbeddingRetriever(embedding_query_service=embedding_query_service)
    finally:
        session.close()
