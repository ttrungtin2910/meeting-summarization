import pytest
from langchain_core.messages import HumanMessage

from ai_agent.graph.nodes.detect_intent import detect_intent


@pytest.mark.parametrize(
    "question, expected_intent",
    [
        # chitchat
        ("Hello!", "chitchat"),
        ("Who are you?", "chitchat"),

        # rag
        ("Why is my record processing failed?", "rag"),

        # out_of_scope
        ("How do you make pizza?", "out_of_scope"),

        # invalid
        ("", "invalid"),
        ("aaaaa", "invalid")
    ])
def test_detect_intent(question, expected_intent):
    """
    Test the detect_intent node with various types of user messages.

    This test ensures that user inputs are correctly classified into one of the predefined intents:
    - chitchat
    - rag
    - action
    - out_of_scope

    Args:
        message (str): The message from the user.
        expected_intent (str): The intent that should be returned by the node.

    Asserts:
        That the returned dictionary contains the correct intent.
    """
    state = {
        "question": question
    }
    result = detect_intent(state)
    assert result["intent"] == expected_intent
