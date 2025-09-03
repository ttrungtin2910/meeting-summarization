"""
Node that summarize the chat history.
"""

from typing import Any, Dict

from langchain_core.messages import BaseMessage

from ai_agent.application.graph.chains import summarize_chain
from ai_agent.application.graph.state import AgentState


def summarize(state: AgentState) -> Dict[str, Any]:
    """
    Summarize the list of chat messages between human and AI
    Args:
        state (AgentState): Contains full conversation as List[BaseMessage]

    Returns:
        Updated AgentState with summary
    """
    messages: list[BaseMessage] = state["messages"]

    if len(messages) == 1:
        return {
            "summary": None
        }

    response = summarize_chain.invoke(messages[:-1])
    return {
        "summary": response
    }
