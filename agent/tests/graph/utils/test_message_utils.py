import pytest
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from ai_agent.graph.utils.message_utils import format_messages


def test_format_messages():
    """
    Convert a list of LangChain BaseMessage objects into a readable multi-line string.

    This function maps the message type (e.g., "human", "ai", "system") to a readable role 
    name ("User", "Assistant", "System") and formats each message into a string like:
    
        User: Hello
        Assistant: Hi! How can I help?

    Args:
        messages (List[BaseMessage]): A list of LangChain BaseMessage objects to be formatted.

    Returns:
        str: A formatted string where each line represents a message with its corresponding role.
    """

    messages = [
        SystemMessage(content="This is a system message."),
        HumanMessage(content="Hello!"),
        AIMessage(content="Hi there! How can I assist you today?")
    ]

    expected_output = (
        "System: This is a system message.\n"
        "User: Hello!\n"
        "Assistant: Hi there! How can I assist you today?"
    )

    assert format_messages(messages) == expected_output
