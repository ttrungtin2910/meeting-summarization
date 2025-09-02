from langchain_core.messages import AIMessage

from ai_agent.graph.core.state import AgentState
from ai_agent.graph.nodes.generate_rag import generate_rag


def test_generate_rag_node_returns_response():
    """
    Test that the generate rag node responds to user input.

    This test verifies that:
    - Given a human greeting message
    - The generate node returns a new AIMessage
    - The message content is a non-empty string
    """
    state = AgentState(
        question="Hi there!",
        summary = None
    )

    result = generate_rag(state)
    assert "messages" in result
    assert isinstance(result["messages"], list)
    assert len(result["messages"]) == 1

    ai_response = result["messages"][0]
    assert isinstance(ai_response, AIMessage)
    assert isinstance(ai_response.content, str)
    assert len(ai_response.content.strip()) > 0