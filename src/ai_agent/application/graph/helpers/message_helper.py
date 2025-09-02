"""Utility functions for messages"""

from typing import List

from langchain_core.messages import BaseMessage


def format_messages(messages: List[BaseMessage]) -> str:
    """
    Convert a list of LangChain BaseMessage objects into a readable string
    for use in PromptTemplate with a {messages} placeholder.

    Args:
        messages (List[BaseMessage]): List of LangChain message objects.

    Returns:
        str: Formatted multi-line string like:
            User: Hello
            Assistant: Hi! How can I help?
    """
    role_map = {
        "human": "User",
        "ai": "Assistant",
        "system": "System"
    }

    lines = [
        f"{role_map.get(msg.type, msg.type)}: {str(msg.content).strip()}"
        for msg in messages
    ]
    return "\n".join(lines)
