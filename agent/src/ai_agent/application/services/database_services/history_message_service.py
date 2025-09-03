"""
History Message Service Module.
"""

from datetime import datetime, timezone
from typing import List
from uuid import UUID

from ai_agent.domain.dtos.history_message_dto import (
    HistoryMessageCreateDTO, HistoryMessageCreateRequestDTO)
from ai_agent.domain.exceptions.chat_session_exceptions import \
    ChatSessionNotFound
from ai_agent.domain.exceptions.history_message_exceptions import \
    HistoryMessageNotFound
from ai_agent.domain.exceptions.organization_exceptions import \
    OrganizationNotFound
from ai_agent.domain.models.database_entities.history_message import \
    HistoryMessage
from ai_agent.infrastructure.database.repositories import (
    BaseChatSessionRepository, BaseHistoryMessageRepository,
    BaseOrganizationRepository)


class HistoryMessageService:
    """
    Service class for managing history message operations.

    This service encapsulates business logic for message history,
    utilizing the repository pattern for data access.
    """

    def __init__(
            self,
            history_message_repository: BaseHistoryMessageRepository,
            chat_session_repository: BaseChatSessionRepository,
            organization_repository: BaseOrganizationRepository
        ):
        """
        Initialize the HistoryMessageService with a history message repository.

        Args:
            history_message_repository (BaseHistoryMessageRepository):
                Data access operations on history messages.
            chat_session_repository (BaseChatSessionRepository):
                Data access operations on chat session.
            organization_repository (BaseOrganizationRepository): repository for organization table
        """
        self.history_message_repository = history_message_repository
        self.chat_session_repository = chat_session_repository
        self.organization_repository = organization_repository

    def create_history_message(
        self,
        data: HistoryMessageCreateRequestDTO,
        organization_id: UUID
    ) -> HistoryMessage:
        """
        Create a new history message.

        Args:
            data (HistoryMessageCreateRequestDTO):
                The message creation data.

        Returns:
            HistoryMessage: The newly created history message.
            organization_id (UUID): ID of the organization

        Raises:
            ChatSessionNotFound: the session does not exists
        """
        # Check if organization exists
        if not self.organization_repository.exists(organization_id=organization_id):
            raise OrganizationNotFound

        # Check if session exists
        session_id = data.session_id
        chat_session = self.chat_session_repository.get(
            session_id,
            organization_id=organization_id
        )
        if not chat_session:
            raise ChatSessionNotFound(session_id)

        message_dto = HistoryMessageCreateDTO(
            **data.model_dump(),
            created_at=datetime.now(tz=timezone.utc),
        )
        return self.history_message_repository.create(
            message_dto,
            organization_id=organization_id
        )

    def get_history_message(
            self,
            message_id: UUID,
            organization_id: UUID
        ) -> HistoryMessage:
        """
        Retrieve a single history message by its ID.

        Args:
            message_id (UUID): The ID of the history message.
            organization_id (UUID): ID of the organization

        Returns:
            HistoryMessage: The retrieved message object.

        Raises:
            HistoryMessageNotFound: If the message does not exist.
        """
        # Check if organization exists
        if not self.organization_repository.exists(organization_id=organization_id):
            raise OrganizationNotFound

        message = self.history_message_repository.get(
            message_id,
            organization_id=organization_id
        )
        if not message:
            raise HistoryMessageNotFound(message_id)
        return message

    def get_list_history_messages(
            self,
            session_id: UUID,
            organization_id: UUID
        ) -> List[HistoryMessage]:
        """
        Retrieve all history messages for a specific session.

        Args:
            session_id (UUID): The ID of the chat session.
            organization_id (UUID): ID of the organization

        Returns:
            List[HistoryMessage]: List of messages for the session.

        Raises:
            ChatSessionNotFound: if the session does not exist
        """
        # Check if session exists
        chat_session = self.chat_session_repository.get(
            session_id=session_id,
            organization_id=organization_id
        )
        if not chat_session:
            raise ChatSessionNotFound(session_id)

        return self.history_message_repository.get_list(
            session_id,
            organization_id=organization_id
        )

    def delete_history_messages(
            self,
            session_id: UUID,
            organization_id: UUID
        ) -> None:
        """
        Delete all history messages associated with a specific session.

        Args:
            session_id (UUID): The ID of the chat session.
            organization_id (UUID): ID of the organization
        """
        # Check if organization exists
        if not self.organization_repository.exists(organization_id=organization_id):
            raise OrganizationNotFound

        # Check if chat session exists
        chat_session = self.chat_session_repository.get(
            session_id,
            organization_id=organization_id
        )
        if not chat_session:
            raise ChatSessionNotFound(session_id)

        self.history_message_repository.delete_by_session(
            session_id,
            organization_id=organization_id
        )
