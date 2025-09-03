"""
Repository for HistoryMessage model.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from ai_agent.domain.dtos.history_message_dto import HistoryMessageCreateDTO
from ai_agent.domain.models.database_entities.history_message import \
    HistoryMessage


class BaseHistoryMessageRepository(ABC):
    """
    Abstract base repository class for managing HistoryMessage model operations.

    This abstract class defines the interface for history message repositories,
    providing methods for CRUD operations related to message history.
    """

    @abstractmethod
    def create(
        self,
        data: HistoryMessageCreateDTO,
        organization_id: UUID
    ) -> HistoryMessage:
        """
        Create a new history message.

        Args:
            data (HistoryMessageCreateRequestDTO): The data required to create the history message.
            organization_id (UUID): ID of the organization

        Returns:
            HistoryMessage: The newly created message object.
        """

    @abstractmethod
    def get(
        self,
        message_id: UUID,
        organization_id: UUID
    ) -> Optional[HistoryMessage]:
        """
        Retrieve a history message by its ID.

        Args:
            message_id (UUID): The UUID of the history message.
            organization_id (UUID): ID of the organization

        Returns:
            Optional[HistoryMessage]: The history message object if found, otherwise None.
        """

    @abstractmethod
    def get_list(
        self,
        session_id: UUID,
        organization_id: UUID
    ) -> List[HistoryMessage]:
        """
        Retrieve all history messages for a specific chat session.

        Args:
            session_id (UUID): The UUID of the chat session.
            organization_id (UUID): ID of the organization

        Returns:
            List[HistoryMessage]: A list of history message objects for the session.
        """

    @abstractmethod
    def delete_by_session(
        self,
        session_id: UUID,
        organization_id: UUID
    ) -> None:
        """
        Delete all history messages associated with a specific chat session.

        Args:
            session_id (UUID): The UUID of the chat session whose messages should be deleted.
            organization_id (UUID): ID of the organization

        Returns:
            None
        """
