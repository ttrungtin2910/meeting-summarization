"""
Node that detects the intent of the user's question.
"""

from typing import Any, Dict

from ai_agent.application.graph.chains import detect_intent_chain
from ai_agent.application.graph.state import AgentState


def detect_intent(state: AgentState) -> Dict[str, Any]:
    """
    Node that detects the intent of the user's question.
    """
    question = state["question"]

    if not question:
        return {"intent": "invalid"}

    # Detect intent using the chain
    result = detect_intent_chain.invoke({"question": question})

    # Return to update the intent
    return {"intent": result.intent}
