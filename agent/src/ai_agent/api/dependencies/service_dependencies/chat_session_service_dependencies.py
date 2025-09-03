"""
Dependency injection module for chat session-related services.
"""

from fastapi import Depends

from ai_agent.api.dependencies.repository_dependencies import (
    get_chat_session_repository, get_collection_repository,
    get_external_user_repository, get_history_message_repository,
    get_organization_repository)
from ai_agent.application.services.database_services import ChatSessionService
from ai_agent.infrastructure.database.repositories import (
    BaseChatSessionRepository, BaseCollectionRepository,
    BaseExternalUserRepository, BaseHistoryMessageRepository,
    BaseOrganizationRepository)


def get_chat_session_service(
    chat_session_repository: BaseChatSessionRepository = Depends(
        get_chat_session_repository),
    history_message_repository: BaseHistoryMessageRepository = Depends(
        get_history_message_repository),
    organization_repository: BaseOrganizationRepository = Depends(
        get_organization_repository
    ),
    collection_repository: BaseCollectionRepository = Depends(
        get_collection_repository
    ),
    external_user_repository: BaseExternalUserRepository = Depends(
        get_external_user_repository
    )
) -> ChatSessionService:
    """
    Factory function that provides a configured ChatSessionService instance.

    Args:
        chat_session_repository (BaseChatSessionRepository): The chat session repository,
            injected via dependency.
        history_message_repository (BaseHistoryMessageRepository): The history message repository,
            injected via dependency.
        organization_repository (BaseOrganizationRepository):
            repository for organization table
        collection_repository (BaseCollectionRepository):
            repository for collection table
        external_user_repository (BaseExternalUserRepository):
            repository for external user table

    Returns:
        ChatSessionService: A configured chat session service ready to manage sessions.
    """
    return ChatSessionService(
        chat_session_repository,
        history_message_repository,
        organization_repository,
        collection_repository,
        external_user_repository
    )
