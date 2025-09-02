"""
Node that generate response user's question is out of scope.
"""

from typing import Any, Dict

from langchain_core.messages import AIMessage

from ai_agent.application.graph.state import AgentState


def out_of_scope(_state: AgentState) -> Dict[str, Any]:
    """
    Handles user inputs that are meaningful but outside the supported system scope.
    (e.g., weather, cooking, general knowledge questions).

    Returns:
        Updated AgentState with an explanation message.
    """
    return {
        "messages": [AIMessage(
            content="I'm sorry, your question seems unrelated to this system."
        )]
    }
