import pytest
from langchain_core.documents import Document
from langchain_core.messages import AIMessage

from ai_agent.graph.chains import generate_rag


@pytest.fixture(name="mock_retriever_fixture")
def mock_retriever():
    """
    Fixture that returns a mock retriever to replace the actual vector store retriever.

    This mock retriever ignores the input query and always returns a fixed list of
    Document objects simulating a relevant retrieval result. It is useful for testing
    RAG pipelines without depending on the real vector index.

    Returns:
        RunnableLambda: A mock retriever that outputs a list of static Documents.
    """
    return [
        Document(page_content=(
            "Welcome to the CPE Document Extraction Platform.\n"
            "To explore its full features, you can register for a free demo at our website.\n"
            "Just click the 'Get a demo' button and fill out your company information."
        ))
    ]


def test_generate_rag_chain_returns_ai_message(monkeypatch, mock_retriever_fixture):
    """
    Integration test for the `generate_rag_chain` LangChain pipeline.

    This test monkeypatches the retriever used inside `generate_rag_chain` with a mock
    retriever that returns static documents. 

    Args:
        monkeypatch (pytest.MonkeyPatch): Built-in pytest fixture for patching module attributes.
        mock_retriever (RunnableLambda): The mocked retriever fixture returning fake documents.

    Asserts:
        - The response is an instance of AIMessage.
        - The response content is not empty.
        - The content includes at least one expected keyword indicating the AI understood the context.
    """
    # Monkeypatch the retriever used in generate_rag
    monkeypatch.setattr(generate_rag, "retriever", mock_retriever_fixture)

    input_data = {
        "question": "How can I start with the website?",
        "history": []
    }

    # Chain is already built at import time
    response = generate_rag.generate_rag_chain.invoke(input_data)

    assert isinstance(response, AIMessage)
    assert len(response.content.strip()) > 0
    assert any(keyword in response.content.lower() for keyword in [
        "demo", "register", "sign up", "book", "start", "free"
    ])
