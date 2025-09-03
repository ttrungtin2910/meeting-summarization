"""
Repository implementation for HistoryMessage model.
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from ai_agent.domain.dtos.history_message_dto import HistoryMessageCreateDTO
from ai_agent.domain.models.database_entities.history_message import \
    HistoryMessage
from ai_agent.infrastructure.database.models import HistoryMessageModel

from .base_history_message_repository import BaseHistoryMessageRepository


class HistoryMessageRepository(BaseHistoryMessageRepository):
    """
    Repository class for managing HistoryMessage model operations in the database.

    This class provides methods to create, retrieve, list, and delete history messages.
    """

    def __init__(self, session: Session):
        """
        Initialize the HistoryMessageRepository with a database session.

        Args:
            session (Session): SQLAlchemy session used for database interaction.
        """
        self.session = session

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
        model = HistoryMessageModel(
            **data.model_dump(),
            organization_id=organization_id,
        )
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return HistoryMessage.model_validate(model)

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
        result = (
            self.session.query(HistoryMessageModel)
            .filter(
                HistoryMessageModel.id == message_id,
                HistoryMessageModel.organization_id == organization_id
            )
            .first()
        )
        if not result:
            return None
        return HistoryMessage.model_validate(result)

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
        results = (
            self.session
            .query(HistoryMessageModel)
            .filter(
                HistoryMessageModel.session_id == session_id,
                HistoryMessageModel.organization_id == organization_id
            )
            .order_by(HistoryMessageModel.created_at.asc())
            .all()
        )
        if not results:
            return []
        return [HistoryMessage.model_validate(row) for row in results]

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
        self.session.query(HistoryMessageModel).filter(
            HistoryMessageModel.session_id == session_id,
            HistoryMessageModel.organization_id == organization_id
        ).delete()
        self.session.commit()
