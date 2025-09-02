"""
ChatSession API endpoints.

This module contains endpoints for managing chat session resources.
"""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from ai_agent.api.dependencies.security_dependencies import get_current_client
from ai_agent.api.dependencies.service_dependencies.chat_session_service_dependencies import \
    get_chat_session_service
from ai_agent.api.schemas.chat_sessions import ChatSessionResponse
from ai_agent.application.services.database_services import ChatSessionService
from ai_agent.domain.dtos.chat_session_dto import (ChatSessionCreateRequestDTO,
                                                   ChatSessionUpdateDTO)
from ai_agent.domain.exceptions.auth_exceptions import InsufficientScope
from ai_agent.domain.exceptions.chat_session_exceptions import \
    ChatSessionNotFound
from ai_agent.domain.exceptions.collection_exceptions import CollectionNotFound
from ai_agent.domain.models.database_entities.chat_session import ChatSession
from ai_agent.domain.models.security_contexts.client_context import \
    ClientContext

router = APIRouter()


@router.post("/chat-sessions", response_model=ChatSessionResponse)
def create_chat_session(
    data: ChatSessionCreateRequestDTO,
    service: ChatSessionService = Depends(get_chat_session_service),
    client_context: ClientContext = Depends(get_current_client),
):
    """
    Create a new chat session.

    Args:
        data (ChatSessionCreateRequestDTO): Session creation payload.

    Returns:
        ChatSessionResponse: The created session object.

    Raises:
        403: If the client does not have the required scope
        404: If the collection does not exist
    """
    try:
        session = service.create_chat_session(data, client_context=client_context)
        return ChatSessionResponse.model_validate(session)

    except InsufficientScope as exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exception)
        ) from exception

    except CollectionNotFound as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exception)
        ) from exception


@router.get("/chat-sessions/{session_id}", response_model=ChatSessionResponse)
def get_chat_session(
    session_id: UUID,
    service: ChatSessionService = Depends(get_chat_session_service),
    client_context: ClientContext = Depends(get_current_client),
):
    """
    Get a specific chat session by ID.

    Args:
        session_id (UUID): Session ID to retrieve.

    Returns:
        ChatSessionResponse: The session data.

    Raises:
        404: If session not found.
        403: If the client does not have the required scope
    """
    try:
        session: ChatSession = service.get_chat_session(
            session_id,
            client_context=client_context
        )
        return ChatSessionResponse.model_validate(session)

    except InsufficientScope as exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exception)
        ) from exception

    except ChatSessionNotFound as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exception)
        ) from exception


@router.get("/chat-sessions/user/{external_user}", response_model=List[ChatSessionResponse])
def get_list_chat_sessions(
    external_user: str,
    service: ChatSessionService = Depends(get_chat_session_service),
    client_context: ClientContext = Depends(get_current_client),
):
    """
    Get list of chat sessions for a user.

    Args:
        external_user (str): user id from other system.

    Returns:
        List[ChatSessionResponse]: List of session objects.

    Raises:
        403: If the client does not have the required scope
    """
    try:
        sessions = service.get_list_chat_session(
            external_user=external_user,
            client_context=client_context
        )
        if not sessions:
            return []
        return [ChatSessionResponse.model_validate(s) for s in sessions]

    except InsufficientScope as exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exception)
        ) from exception


@router.patch("/chat-sessions/{session_id}", response_model=ChatSessionResponse)
def update_chat_session(
    session_id: UUID,
    data: ChatSessionUpdateDTO,
    service: ChatSessionService = Depends(get_chat_session_service),
    client_context: ClientContext = Depends(get_current_client),
):
    """
    Update a chat session by ID.

    Args:
        session_id (UUID): ID of the session.
        data (ChatSessionUpdateDTO): Updated session fields.

    Returns:
        ChatSessionResponse: The updated session.

    Raises:
        404: If session not found.
        403: If the client does not have the required scope
    """
    try:
        updated = service.update_chat_session(session_id, data, client_context=client_context)
        return ChatSessionResponse.model_validate(updated)

    except InsufficientScope as exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exception)
        ) from exception

    except ChatSessionNotFound as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exception)
        ) from exception


@router.delete("/chat-sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chat_session(
    session_id: UUID,
    service: ChatSessionService = Depends(get_chat_session_service),
    client_context: ClientContext = Depends(get_current_client),
):
    """
    Delete a chat session by ID.

    Args:
        session_id (UUID): ID of the session to delete.

    Raises:
        404: If session not found.
        403: If the client does not have the required scope
    """
    try:
        service.delete_chat_session(session_id, client_context=client_context)

    except InsufficientScope as exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exception)
        ) from exception

    except ChatSessionNotFound as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exception)
        ) from exception
