"""Chat API"""

from typing import List
from uuid import UUID

from fastapi import (APIRouter, Body, Depends, HTTPException, Path, Query,
                     status)

from ai_agent.api.dependencies.security_dependencies import get_current_client
from ai_agent.api.dependencies.service_dependencies.chat_service_dependencies import \
    get_chat_service
from ai_agent.api.helpers.message_converter import (
    convert_all_to_chat_messages, convert_to_chat_message)
from ai_agent.api.schemas.chat import (ChatRequest, ChatRequestMessage,
                                       ChatResponse)
from ai_agent.application.services.chat_service import ChatService
from ai_agent.domain.exceptions.auth_exceptions import InsufficientScope
from ai_agent.domain.exceptions.chat_session_exceptions import \
    ChatSessionNotFound
from ai_agent.domain.exceptions.message_exceptions import MessageNotFound
from ai_agent.domain.models.security_contexts.client_context import \
    ClientContext
from ai_agent.domain.value_objects.chat_message import ChatMessage

router = APIRouter()


@router.post('/chat', response_model=ChatResponse)
def chat(
    request: ChatRequest,
    service: ChatService = Depends(get_chat_service),
    collection_ids: List[UUID] = Query(
        ...,
        description="Collections for agent to get data for the conversation"
    ),
    client_context: ClientContext = Depends(get_current_client),
):
    """
    Handles chat requests by processing messages and returning a response.

    This endpoint receives a chat request, processes the messages using the specified chat service,
    and returns a chat response. If the messages cannot be processed,
    a default error message is returned.

    Parameters:
        request (ChatRequest): The chat request containing messages to be processed.
        collection_ids (List[UUID]): The IDs of the collections from which the agent retrieves data
                                        for the conversation. This is optional.

    Returns:
        ChatResponse: The response containing the processed chat content
            or an error message if processing fails.

    Raises:
        MessageNotFound: If the messages cannot be found or processed,
            an error message is returned in the response.
        403: If the client does not have the required scope
    """
    try:
        # Convert messages to ChatMessage object
        chat_messages: List[ChatMessage] = convert_all_to_chat_messages(request.messages)
        result = service.chat(
            chat_messages,
            collection_ids=collection_ids,
            client_context=client_context
        )
        return ChatResponse(content=str(result.content))

    except InsufficientScope as exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exception)
        ) from exception

    except MessageNotFound:
        return ChatResponse(content="Sorry, I could not help at the moment.")


@router.post(
    "/chat/sessions/{session_id}",
    response_model=ChatResponse
)
def chat_with_session(
    session_id: UUID = Path(..., description="ID of the history chat session"),
    message: ChatRequestMessage = Body(..., description="The last message from user"),
    service: ChatService = Depends(get_chat_service),
    client_context: ClientContext = Depends(get_current_client),
):
    """
    Send a chat message within a specific chat session.

    This endpoint processes a single message from user,
    get history from the database based on session_id

    Args:
        session_id (UUID): The unique identifier of the chat session
        message (ChatRequestMessage): The message from the user

    Returns:
        ChatResponse: The AI's response content

    Raises:
        400: If the specified chat session does not exist
        403: If the client does not have the required scope

    Notes:
        - The session history is automatically loaded and maintained
        - Both the user message and AI response are saved to the session history
    """
    try:
        chat_message: ChatMessage = convert_to_chat_message(message)
        result = service.chat_with_session(
            session_id,
            input_message=chat_message,
            client_context=client_context
        )
        return ChatResponse(content=str(result.content))

    except InsufficientScope as exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exception)
        ) from exception

    except ChatSessionNotFound as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exception)
        ) from exception

    except MessageNotFound:
        return ChatResponse(content="Sorry, I could not help at the moment.")
