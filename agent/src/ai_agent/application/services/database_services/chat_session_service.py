"""
ChatSession Service Module.
"""

from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID

from ai_agent.domain.dtos.chat_session_dto import (ChatSessionCreateDTO,
                                                   ChatSessionCreateRequestDTO,
                                                   ChatSessionUpdateDTO)
from ai_agent.domain.exceptions.chat_session_exceptions import \
    ChatSessionNotFound
from ai_agent.domain.exceptions.collection_exceptions import CollectionNotFound
from ai_agent.domain.exceptions.external_user_exceptions import \
    ExternalUserNotFound
from ai_agent.domain.models.database_entities.chat_session import ChatSession
from ai_agent.domain.models.security_contexts.client_context import \
    ClientContext
from ai_agent.infrastructure.database.repositories import (
    BaseChatSessionRepository, BaseCollectionRepository,
    BaseExternalUserRepository, BaseHistoryMessageRepository,
    BaseOrganizationRepository)


class ChatSessionService:
    """
    Service class for managing chat session operations.

    This service encapsulates business logic for chat session management,
    utilizing the repository pattern for data access.
    """

    def __init__(
            self,
            chat_session_repository: BaseChatSessionRepository,
            history_message_repository: BaseHistoryMessageRepository,
            organization_repository: BaseOrganizationRepository,
            collection_repository: BaseCollectionRepository,
            external_user_repository: BaseExternalUserRepository,

        ):
        """
        Initialize the ChatSessionService with a chat session repository.

        Args:
            chat_session_repository (BaseChatSessionRepository):
                Interface used for data access operations on chat sessions.
            history_message_repository (BaseHistoryMessageRepository):
                Interface used for working with history message table.
            organization_repository (BaseOrganizationRepository): repository for organization table
            collection_repository (BaseCollectionRepository):
                Repository to work with the collection table.
            external_user_repository (BaseExternalUserRepository):
                Repository to work with external user table
        """
        self.chat_session_repository = chat_session_repository
        self.history_message_repository = history_message_repository
        self.organization_repository = organization_repository
        self.collection_repository = collection_repository
        self.external_user_repository = external_user_repository

    def create_chat_session(
            self,
            data: ChatSessionCreateRequestDTO,
            client_context: ClientContext
        ) -> ChatSession:
        """
        Create a new chat session.

        Args:
            data (ChatSessionCreateRequestDTO): The session creation data.
            client_context (ClientContext): The authenticated client

        Returns:
            ChatSession: The newly created chat session.
        """
        organization_id = client_context.organization_id

        # Get or create external user
        current_external_user = self.get_or_create_external_user(
            data.external_user,
            organization_id=organization_id,
            client_id=client_context.client_id
        )

        # If request has collection_ids, check if exists in app client collection ids
        if data.collection_ids:
            existed_collection_ids = client_context.collection_ids
            for collection_id in data.collection_ids:
                if collection_id not in existed_collection_ids:
                    raise CollectionNotFound(collection_id=collection_id)
            collection_ids = data.collection_ids
        # if request does does not have collection_ids, use app client's collection ids
        else:
            collection_ids = client_context.collection_ids
        session_dto = ChatSessionCreateDTO(
            external_user_id=current_external_user.id,
            client_id=client_context.client_id,
            organization_id=organization_id,
            collection_ids=collection_ids,
            created_at=datetime.now(tz=timezone.utc),
            updated_at=datetime.now(tz=timezone.utc),
        )
        return self.chat_session_repository.create(session_dto)

    def get_chat_session(
            self,
            session_id: UUID,
            client_context: ClientContext
        ) -> ChatSession:
        """
        Retrieve a single chat session by its ID.

        Args:
            session_id (UUID): The ID of the session.
            client_context (ClientContext): The authenticated client

        Returns:
            ChatSession: The retrieved session object.

        Raises:
            ChatSessionNotFound: If the session does not exist.
        """
        session: Optional[ChatSession] = self.chat_session_repository.get(session_id)
        if not session or client_context.client_id != session.client_id:
            raise ChatSessionNotFound(session_id)
        return session

    def get_list_chat_session(
            self,
            external_user: str,
            client_context: ClientContext
        ) -> List[ChatSession]:
        """
        Retrieve all chat sessions for a given user.

        Args:
            external_user (str): The user from other system.
            client_context (ClientContext): The authenticated client

        Returns:
            List[ChatSession]: List of chat sessions.
        """
        organization_id = client_context.organization_id
        current_external_user = self.external_user_repository.get_by_external_user(
            external_user=external_user,
            organization_id=organization_id,
            client_id=client_context.client_id
        )
        if not current_external_user:
            raise ExternalUserNotFound()

        return self.chat_session_repository.get_list(
            current_external_user.id
        )

    def update_chat_session(
            self,
            session_id: UUID,
            data: ChatSessionUpdateDTO,
            client_context: ClientContext
        ) -> ChatSession:
        """
        Update an existing chat session.

        Args:
            session_id (UUID): The ID of the session.
            data (ChatSessionUpdateDTO): The data to update.
            client_context (ClientContext): The authenticated client

        Returns:
            ChatSession: The updated session.

        Raises:
            ChatSessionNotFound: If the session does not exist.
        """
        session = self.chat_session_repository.get(
            session_id,
        )
        if not session or client_context.client_id != session.client_id:
            raise ChatSessionNotFound(session_id)

        # Check if any field has changed
        has_changed = False
        update_data = data.model_dump(exclude_unset=True, exclude_none=True)
        for field, new_value in update_data.items():
            old_value = getattr(session, field, None)
            if new_value != old_value:
                has_changed = True
                break

        if not has_changed:
            return session

        updated = self.chat_session_repository.update(
            session_id,
            data,
        )
        assert updated is not None
        return updated


    def delete_chat_session(
            self,
            session_id: UUID,
            client_context: ClientContext
        ) -> None:
        """
        Delete a chat session by its ID.

        Args:
            session_id (UUID): The ID of the session to delete.
            client_context (ClientContext): The authenticated client

        Raises:
            ChatSessionNotFound: If the session does not exist.
        """
        # Check if session exists
        organization_id = client_context.organization_id
        chat_session = self.chat_session_repository.get(
            session_id,
        )
        if not chat_session or chat_session.client_id != client_context.client_id:
            raise ChatSessionNotFound(session_id)

        # Check if history messages exist, delete history messages
        history_messages = self.history_message_repository.get_list(
            session_id,
            organization_id=organization_id
        )
        if history_messages:
            self.history_message_repository.delete_by_session(
                session_id,
                organization_id=organization_id
            )

        self.chat_session_repository.delete(
            session_id,
        )

    def get_or_create_external_user(
            self,
            external_user: str,
            organization_id: UUID,
            client_id: UUID
    ):
        """
        Retrieves an external user associated with the given organization, or
        creates a new one if it does not exist.

        Args:
            external_user (str): The identifier for the external user to be
                retrieved or created.
            organization_id (UUID): The unique identifier of the organization
                associated with the external user.
            client_id (UUID): ID of the app_client created the chat session

        Returns:
            ExternalUser: The external user object, either retrieved from the
                repository or newly created.
        """
        current_external_user = self.external_user_repository.get_by_external_user(
            external_user=external_user,
            organization_id=organization_id,
            client_id=client_id
        )
        if not current_external_user:
            current_external_user = self.external_user_repository.create(
                external_user=external_user,
                organization_id=organization_id,
                client_id=client_id
            )
        return current_external_user
