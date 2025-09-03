"""
Node that generate response if user's question is invalid.
"""

from typing import Any, Dict

from langchain_core.messages import AIMessage

from ai_agent.application.graph.state import AgentState


def invalid(_state: AgentState) -> Dict[str, Any]:
    """
    Handles user inputs that are classified as 'invalid'.

    This may include empty strings, gibberish, spam-like content, or inputs that
    do not resemble any meaningful query.

    Returns:
        Updated AgentState with a polite message
    """
    return {
        "messages": [AIMessage(
            content="Sorry, I couldn't understand your message."
        )]
    }
