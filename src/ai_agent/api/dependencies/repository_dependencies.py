"""
Dependency injection module for database repository
"""

from fastapi import Depends
from sqlalchemy.orm import Session

from ai_agent.infrastructure.database.base.session import get_db
from ai_agent.infrastructure.database.repositories import (
    AdminRepository, AppClientRepository, BaseAdminRepository,
    BaseAppClientRepository, BaseCategoryRepository, BaseChatSessionRepository,
    BaseCollectionRepository, BaseDocumentRepository, BaseEmbeddingRepository,
    BaseExternalUserRepository, BaseHistoryMessageRepository,
    BaseOrganizationRepository, CategoryRepository, ChatSessionRepository,
    CollectionRepository, DocumentRepository, EmbeddingRepository,
    ExternalUserRepository, HistoryMessageRepository, OrganizationRepository)


def get_collection_repository(
    session: Session = Depends(get_db),
) -> BaseCollectionRepository:
    """
    Provides a BaseCollectionRepository instance.

    Args:
        session (Session): session

    Returns:
        BaseCollectionRepository: Repository for collection-related operations
    """
    return CollectionRepository(session)


def get_category_repository(
        session: Session = Depends(get_db)
    ) -> BaseCategoryRepository:
    """
    Provides a BaseCategoryRepository instance.

    Args:
        session (Session): session

    Returns:
        CategoryRepository: Repository for category-related operations
    """
    return CategoryRepository(session)


def get_document_repository(
        session: Session = Depends(get_db)
) -> BaseDocumentRepository:
    """
    Provides a BaseDocumentRepository instance.

    Args:
        session (Session): session

    Returns:
        BaseDocumentRepository: Repository for document-related operations
    """
    return DocumentRepository(session)


def get_embedding_repository(
        session: Session = Depends(get_db)
) -> BaseEmbeddingRepository:
    """
    Provides a BaseEmbeddingRepository instance.

    Args:
        session (Session): session

    Returns:
        BaseEmbeddingRepository: Repository for document-related operations
    """
    return EmbeddingRepository(session)


def get_chat_session_repository(
        session: Session = Depends(get_db)
) -> BaseChatSessionRepository:
    """
    Provides a BaseChatSessionRepository instance.

    Args:
        session (Session): session

    Returns:
        BaseChatSessionRepository: Repository for document-related operations
    """
    return ChatSessionRepository(session)


def get_history_message_repository(
        session: Session = Depends(get_db)
) -> BaseHistoryMessageRepository:
    """
    Provides a BaseHistoryMessageRepository instance.

    Args:
        session (Session): session

    Returns:
        BaseHistoryMessageRepository: Repository for history message operations
    """
    return HistoryMessageRepository(session)


def get_organization_repository(
    session: Session = Depends(get_db)
) -> BaseOrganizationRepository:
    """
    Provides an BaseOrganizationRepository instance.

    Args:
        session (Session): session

    Returns:
        BaseOrganizationRepository: Repository for organization operations
    """
    return OrganizationRepository(session)


def get_app_client_repository(
    session: Session = Depends(get_db),
) -> BaseAppClientRepository:
    """
    Provides an BaseAppClientRepository instance.

    Args:
        session (Session): SQLAlchemy session.

    Returns:
        BaseAppClientRepository: Repository for AppClient table.
    """
    return AppClientRepository(session)

def get_external_user_repository(
        session: Session = Depends(get_db)
    ) -> BaseExternalUserRepository:
    """
    Provides an instance of the BaseExternalUserRepository with database session.

    Args:
        db (Session): SQLAlchemy database session.

    Returns:
        BaseExternalUserRepository: The concrete implementation for external users.
    """
    return ExternalUserRepository(session)

def get_admin_repository(
        session: Session = Depends(get_db)
) -> BaseAdminRepository:
    """
    Provides an instance of the BaseAdminRepository with database session.

    Args:
        db (Session): SQLAlchemy database session.

    Returns:
        BaseAdminRepository: The concrete implementation for admin.
    """
    return AdminRepository(session)
