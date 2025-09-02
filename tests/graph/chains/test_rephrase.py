from langchain_core.messages import AIMessage, HumanMessage

from ai_agent.graph.chains.rephrase import rephrase_chain


def test_rephrase_chain_return_history_topic():
    """
    Integration test for `rephrase_chain`

    This test simulates that the chat history is about cat topic,
    the final question only includes "how about blue?"

    Expected answer must include the word "cat"
    """
    input_data = {
        "summary": "User wants to buy a cat. AI asks about the color, and the user responds red. AI says red is lovely.",
        "question": "how about blue?"
    }

    response = rephrase_chain.invoke(input_data)
    assert isinstance(response, str)
    assert "cat" in response.lower()

