"""
Model for intent detection.
"""

from typing import Literal

from pydantic import BaseModel, Field


class DetectIntentOutput(BaseModel):
    """
    Structured output format used by the detect_intent chain.

    Attributes:
        intent: The type of user query intent. One of: chitchat, rag, action, out_of_scope, invalid.
    """
    intent: Literal["chitchat", "rag", "action", "out_of_scope", "invalid"] = Field(
        ...,
        description="The user query intent. \
            One of: 'chitchat', 'rag', 'action', 'out_of_scope', 'invalid'."
    )
