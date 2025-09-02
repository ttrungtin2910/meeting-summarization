"""
Chat Message Models Module.

This module defines the core data models for representing chat messages
in conversational AI applications.
"""

from enum import Enum
from typing import Union

from pydantic import BaseModel


class ChatRole(Enum):
    """
    Enumeration of possible roles in a chat conversation.

    This enum defines the different participants in a chat interaction:
    - HUMAN: Represents messages from the user
    - AI: Represents messages from the AI assistant
    """
    HUMAN = "human"
    AI = "ai"
    SYSTEM = "system"


class ChatMessage(BaseModel):
    """
    Model representing a single message in a chat conversation.

    Each chat message contains the role of the sender (human or AI)
    and the text content of the message.

    Attributes:
        type (ChatRole): The role of the entity sending the message (human or AI)
        content (Union[str, list[Union[str, dict]]]): The text content of the message

    Example:
        message = ChatMessage(type=ChatRole.HUMAN, content="How does this work?")
    """
    type: ChatRole
    content: Union[str, list[Union[str, dict]]]
