"""
Repository class for managing ChatSession model operations in the database.

This module provides a concrete implementation of BaseChatSessionRepository,
using SQLAlchemy ORM for performing CRUD operations on ChatSession entities.
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import select

from ai_agent.domain.dtos.chat_session_dto import (ChatSessionCreateDTO,
                                                   ChatSessionUpdateDTO)
from ai_agent.domain.models.database_entities.chat_session import ChatSession
from ai_agent.infrastructure.database.models import ChatSessionModel
from ai_agent.infrastructure.database.models.collection_model import CollectionModel

from .base_chat_session_repository import BaseChatSessionRepository


class ChatSessionRepository(BaseChatSessionRepository):
    """
    Repository class for ChatSession model.

    This class provides methods to create, retrieve, list, update, and delete ChatSession records
    in the database.
    """

    def __init__(
            self,
            session: Session,
        ):
        """
        Initialize the ChatSessionRepository with a database session.

        Args:
            session (Session): SQLAlchemy database session.
        """
        self.session = session

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
        statement = (
            select(CollectionModel)
            .where(
                CollectionModel.id.in_(data.collection_ids)
            )
        )
        collections: List[CollectionModel] = self.session.execute(statement).scalars().all()
        session_model = ChatSessionModel(
            **data.model_dump(exclude={"collection_ids"}),
            collections=collections
        )
        self.session.add(session_model)
        self.session.commit()
        self.session.refresh(session_model)
        return ChatSession.model_validate(session_model)

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
        result = (
            self.session.query(ChatSessionModel)
            .filter(
                ChatSessionModel.id==session_id,
            )
            .first()
        )
        if not result:
            return None
        return ChatSession.model_validate(result)

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
        results = (
            self.session.query(ChatSessionModel)
            .filter(
                ChatSessionModel.external_user_id==external_user_id,
            )
            .all()
        )
        if not results:
            return []
        return [ChatSession.model_validate(item) for item in results]

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
        session_obj = (
            self.session.query(ChatSessionModel)
            .filter(
                ChatSessionModel.id==session_id,
            )
            .first()
        )
        if not session_obj:
            return None

        update_data = data.model_dump(exclude_unset=True, exclude_none=True)
        for key, value in update_data.items():
            setattr(session_obj, key, value)

        self.session.commit()
        self.session.refresh(session_obj)
        return ChatSession.model_validate(session_obj)

    def delete(
        self,
        session_id: UUID,
    ) -> None:
        """
        Delete a chat session by its ID.

        Args:
            session_id (UUID): The UUID of the chat session to delete.

        Returns:
            None
        """
        session_obj = (
            self.session.query(ChatSessionModel)
            .filter(
                ChatSessionModel.id==session_id,
            )
            .first()
        )
        if session_obj:
            self.session.delete(session_obj)
            self.session.commit()
