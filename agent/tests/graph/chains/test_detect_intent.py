import pytest

from ai_agent.graph.chains.detect_intent import detect_intent_chain


@pytest.mark.parametrize("question, expected_intent", [
    # Chitchat
    ("Hello, I need help", "chitchat"),

    # rag
    ("How to create a parsing rule", "rag"),
    ("What steps do I need to take to extract a passport?", "rag"),

    # out of scope
    ("What is the weather today?", "out_of_scope"),
    ("Do you like trump of biden?", "out_of_scope"),
    ("How to make pizza?", "out_of_scope"),

    # invalid
    ("", "invalid"),
    ("abccc", "invalid")
])
def test_detect_intent_chain(question, expected_intent):
    """Test if detect_intent_chain returns correct intent for various queries."""
    result = detect_intent_chain.invoke({"question": question})
    assert result.intent == expected_intent, f"Expected: {expected_intent}, got: {result.intent}"