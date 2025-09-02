"""
Node that retrieve data from vector store for answer user's question.
"""

from typing import Any, Dict

from ai_agent.application.graph.state import AgentState
from ai_agent.infrastructure.vector_storage import get_vector_storage

storage = get_vector_storage()
retriever = storage.as_retriever()

def retrieve(state: AgentState) -> Dict[str, Any]:
    """
    Retrieve relevant documents based on the latest human message.

    This function looks for the last human message in the conversation history,
    and uses its content as a query to retrieve relevant documents via the retriever.

    If no human message is found, it returns a result with None.

    Args:
        state (AgentState): The current agent state containing conversation messages.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - "rag_docs": list of retrieved documents, or None if no valid message found.
    """
    last_human_message = next(
        (msg for msg in reversed(state["messages"]) if msg.type == "human"), None
    )

    if not last_human_message:
        return {
            "rag_docs": None
        }

    documents = retriever.invoke(last_human_message.content)
    return {
        "rag_docs": documents
    }
