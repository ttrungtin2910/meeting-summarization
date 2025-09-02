from langchain_core.messages import AIMessage, HumanMessage

from ai_agent.graph.chains.summarize import summarize_chain


def test_summarize_chain():
    """
    Integration test for `summarize chain`
    """

    messages = [
        HumanMessage(content="I want to process a passport!"),
        AIMessage(content="Yes, you need to request a demo and then create a parsing rule " \
        "to extract the relevant information from the passport document."),
        HumanMessage(content="Can I use Vietnamese")
    ]

    response = summarize_chain.invoke(messages)

    assert isinstance(response, str)
    assert all(keyword in response.lower() for keyword in [
        "demo", "passport", "vietnamese"
    ])
