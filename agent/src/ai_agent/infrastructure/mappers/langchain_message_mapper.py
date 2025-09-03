"""
chat_message_mapper.py

This module provides utility functions to convert between the internal domain
representation of chat messages (`ChatMessage`) and LangChain's external message
format (`BaseMessage`, e.g., `HumanMessage`, `AIMessage`).
"""

from typing import List

from langchain_core.messages import (AIMessage, BaseMessage, HumanMessage,
                                     SystemMessage)

from ai_agent.domain.value_objects.chat_message import ChatMessage, ChatRole


def convert_to_langchain_message(message: ChatMessage) -> BaseMessage:
    """
    Convert a ChatMessage (internal format) to LangChain BaseMessage.

    Args:
        msg (ChatMessage): The internal message format.

    Returns:
        BaseMessage: The equivalent LangChain message.
    """
    if message.type == ChatRole.HUMAN:
        return HumanMessage(
            content=message.content
        )

    if message.type == ChatRole.AI:
        return AIMessage(
            content=message.content
        )

    if message.type == ChatRole.SYSTEM:
        return SystemMessage(
            content=message.content
        )

    raise ValueError(f"Unsupported role: {message.type}")

def convert_from_langchain_message(message: BaseMessage) -> ChatMessage:
    """
    Convert a LangChain BaseMessage to ChatMessage (internal format),
    using `type` field to infer the role.

    Args:
        message (BaseMessage): The LangChain message.

    Returns:
        ChatMessage: The equivalent internal chat message.

    Raises:
        ValueError: If the message type is not supported.
    """
    mapper = {
        "human": ChatRole.HUMAN,
        "ai": ChatRole.AI,
        "system": ChatRole.SYSTEM
    }

    message_type = mapper.get(message.type)
    if message_type is None:
        raise ValueError(f"Unsupported message type: {message.type}")

    return ChatMessage(type=message_type, content=message.content)


def convert_to_langchain_messages(messages: List[ChatMessage]) -> List[BaseMessage]:
    """
    Convert a list of ChatMessage objects to LangChain BaseMessages.

    Args:
        messages (List[ChatMessage]): List of internal chat messages.

    Returns:
        List[BaseMessage]: Equivalent list of LangChain messages.
    """
    return [convert_to_langchain_message(message) for message in messages]


def convert_from_langchain_messages(messages: List[BaseMessage]) -> List[ChatMessage]:
    """
    Convert a list of LangChain BaseMessages to ChatMessage objects.

    Args:
        messages (List[BaseMessage]): List of LangChain messages.

    Returns:
        List[ChatMessage]: Equivalent internal chat messages.
    """
    return [convert_from_langchain_message(message) for message in messages]
