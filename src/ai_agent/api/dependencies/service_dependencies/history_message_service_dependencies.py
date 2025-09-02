"""
Dependency injection module for history message-related services.
"""

from fastapi import Depends

from ai_agent.api.dependencies.repository_dependencies import (
    get_chat_session_repository, get_history_message_repository,
    get_organization_repository)
from ai_agent.application.services.database_services import \
    HistoryMessageService
from ai_agent.infrastructure.database.repositories import (
    BaseChatSessionRepository, BaseHistoryMessageRepository,
    BaseOrganizationRepository)


def get_history_message_service(
    history_message_repository: BaseHistoryMessageRepository = Depends(
        get_history_message_repository
    ),
    chat_session_repository: BaseChatSessionRepository = Depends(
        get_chat_session_repository
    ),
    organization_repository: BaseOrganizationRepository = Depends(
        get_organization_repository
    )
) -> HistoryMessageService:
    """
    Factory function that provides a configured HistoryMessageService instance.

    Args:
        history_message_repository (BaseHistoryMessageRepository): The history message repository,
            injected via dependency.
        chat_session_repository (BaseChatSessionRepository): The chat session repository,
            injected via dependency.
        organization_repository (BaseOrganizationRepository):
            repository for organization table

    Returns:
        HistoryMessageService: A configured history message service ready to manage sessions.
    """
    return HistoryMessageService(
        history_message_repository,
        chat_session_repository,
        organization_repository
    )
