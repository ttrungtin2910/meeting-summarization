"""
Node that rephrase the user's question.
"""

from typing import Any, Dict

from langchain_core.messages import BaseMessage

from ai_agent.application.graph.chains import rephrase_chain
from ai_agent.application.graph.state import AgentState


def rephrase(state: AgentState) -> Dict[str, Any]:
    """
    Rephrase the last question from human.

    Args:
        state (AgentState): Contains full conversation as List[BaseMessage]

    Returns:
        Updated AgentState with new question
    """
    messages: list[BaseMessage] = state["messages"]

    if len(messages) == 1:
        return {
            "question": messages[0].content
        }

    # Extract history and the last question
    summary = state["summary"]
    question = messages[-1].content.strip() if isinstance(messages[-1].content, str) else None

    if not question:
        return {
            "question": ""
        }

    rephrased_question = rephrase_chain.invoke({
        "summary": summary,
        "question": question,
    })
    return {
        "question": rephrased_question
    }
