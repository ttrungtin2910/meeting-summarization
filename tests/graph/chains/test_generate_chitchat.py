from langchain_core.messages import AIMessage, HumanMessage

from ai_agent.graph.chains.generate_chitchat import generate_chitchat_chain


def test_generate_chitchat_chain_returns_ai_message():
    """
    Integration test for `generate_chain`

    This test simulates a user on the CPE website asking a simple question
    """
    question = "Who are you?"
    summary = "User asks about how to start using the system. AI responds that the user can request for a demo version."

    response = generate_chitchat_chain.invoke({
        "question": question,
        "summary": summary
    })

    assert isinstance(response, AIMessage)
    assert len(response.content.strip()) > 0
