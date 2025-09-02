"""Utilities for converting messages"""

from typing import List

from ai_agent.api.schemas.chat import ChatRequestMessage
from ai_agent.domain.value_objects.chat_message import ChatMessage, ChatRole


def convert_to_chat_message(message: ChatRequestMessage) -> ChatMessage:
    """
    Convert an API request message to an internal ChatMessage.

    Args:
        message (ChatRequestMessage): The API message to convert

    Returns:
        ChatMessage: The converted internal chat message

    Raises:
        ValueError: If the message type is not supported (not 'human' or 'ai')
    """
    if message.type == ChatRole.HUMAN:
        return ChatMessage(
            type=ChatRole.HUMAN,
            content=message.content
        )
    if message.type == ChatRole.AI:
        return ChatMessage(
            type=ChatRole.AI,
            content=message.content
        )
    raise ValueError(f"Do not support the message type: {message.type}")


def convert_all_to_chat_messages(messages: List[ChatRequestMessage]) -> List[ChatMessage]:
    """
    Convert a list of API request messages to internal ChatMessage objects.

    Args:
        messages (List[ChatRequestMessage]): List of API messages to convert

    Returns:
        List[ChatMessage]: List of converted internal chat messages
    """
    return [convert_to_chat_message(message) for message in messages]
