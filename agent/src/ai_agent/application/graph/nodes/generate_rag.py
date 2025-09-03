"""
Node that generate response for user's question using RAG.
"""

from typing import Any, Dict

from ai_agent.application.graph.chains import generate_rag_chain
from ai_agent.application.graph.state import AgentState


def generate_rag(state: AgentState) -> Dict[str, Any]:
    """
    Responds to user question with RAG.

    Args:
        state (AgentState): Contains full conversation as List[BaseMessage]

    Returns:
        Updated AgentState with new AIMessage response
    """
    question = state["question"]
    summary = state["summary"]
    collection_ids = state["collection_ids"]
    organization_id = state["organization_id"]

    response = generate_rag_chain.invoke({
        "question": question,
        "history": summary,
        "collection_ids": collection_ids,
        "organization_id": organization_id
    })
    return {
        "messages": [response]
    }
