from langchain_core.messages import AIMessage, HumanMessage

from ai_agent.graph.core.state import AgentState
from ai_agent.graph.nodes.generate_chitchat import generate_chitchat


def test_generate_chitchat_node_returns_response():
    """
    Test that the generate chitchat node responds to user input.

    This test verifies that:
    - Given a human greeting message
    - The generate node returns a new AIMessage
    - The message content is a non-empty string
    """
    state = AgentState(
        question="Hi there!",
        summary=""
    )

    result = generate_chitchat(state)
    assert "messages" in result
    assert isinstance(result["messages"], list)
    assert len(result["messages"]) == 1

    ai_response = result["messages"][0]
    assert isinstance(ai_response, AIMessage)
    assert isinstance(ai_response.content, str)
    assert len(ai_response.content.strip()) > 0