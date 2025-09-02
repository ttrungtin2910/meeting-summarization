"""
Node that generate response for user's chitchat.
"""

from typing import Any, Dict

from ai_agent.application.graph.chains import generate_chitchat_chain
from ai_agent.application.graph.state import AgentState


def generate_chitchat(state: AgentState) -> Dict[str, Any]:
    """
    Responds to user chitchat.

    Args:
        state (AgentState): Contains full conversation as List[BaseMessage]

    Returns:
        Updated AgentState with new AIMessage response
    """
    question = state["question"]
    summary = state["summary"]

    response = generate_chitchat_chain.invoke({
        "question": question,
        "summary": summary
    })
    return {
        "messages": [response]
    }
