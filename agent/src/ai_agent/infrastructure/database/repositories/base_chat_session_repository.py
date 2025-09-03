"""
Repository for ChatSession model.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from ai_agent.domain.dtos.chat_session_dto import (ChatSessionCreateDTO,
                                                   ChatSessionUpdateDTO)
from ai_agent.domain.models.database_entities.chat_session import ChatSession


class BaseChatSessionRepository(ABC):
    """
    Abstract base repository class for managing ChatSession model operations.

    This abstract class defines the interface for ChatSession repositories,
    providing methods for CRUD operations on ChatSession entities.
    """

    @abstractmethod
    def create(
        self,
        data: ChatSessionCreateDTO,
    ) -> ChatSession:
        """
        Create a new chat session.

        Args:
            data (ChatSessionCreateDTO): The data required to create the chat session,

        Returns:
            ChatSession: The newly created chat session object.
        """

    @abstractmethod
    def get(
        self,
        session_id: UUID,
    ) -> Optional[ChatSession]:
        """
        Retrieve a chat session by its ID.

        Args:
            session_id (UUID): The UUID of the chat session to retrieve.

        Returns:
            Optional[ChatSession]: The chat session object if found, otherwise None.
        """

    @abstractmethod
    def get_list(
        self,
        external_user_id: UUID,
    ) -> List[ChatSession]:
        """
        Retrieve all chat sessions for a specific user.

        Args:
            external_user_id (UUID): The UUID of the user whose chat sessions are to be retrieved.

        Returns:
            List[ChatSession]: A list of chat session objects for the user.
        """

    @abstractmethod
    def update(
        self,
        session_id: UUID,
        data: ChatSessionUpdateDTO,
    ) -> Optional[ChatSession]:
        """
        Update a chat session with new data.

        Args:
            session_id (UUID): The UUID of the chat session to update.
            data (ChatSessionUpdateDTO): The fields to update the chat session with,
                including (optionally):
                - name (str): The new name of the session.

        Returns:
            Optional[ChatSession]: The updated chat session object if found, otherwise None.
        """

    @abstractmethod
    def delete(
        self,
        session_id: UUID,
    ) -> None:
        """
        Delete a chat session by its ID.

        Args:
            session_id (UUID): The UUID of the chat session to delete.
            organization_id (UUID): ID of the organization

        Returns:
            None
        """
