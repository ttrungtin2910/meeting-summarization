"""Models for Chat API"""

from typing import List

from pydantic import BaseModel

from ai_agent.domain.value_objects.chat_message import ChatRole


class ChatRequestMessage(BaseModel):
    """
    Represents a single message in a conversation history.

    Attributes:
        type (ChatRole): The role of the message sender. Either "human" or "ai".
        content (str): The actual message text.
    """
    type: ChatRole
    content: str


class ChatRequest(BaseModel):
    """
    Schema representing a chat request from the frontend (e.g., CopilotKit or a chat UI).
    Attributes:
        messages (List[BaseMessage]):
            A list of messages in the current conversation.
            Each message should include type (e.g., 'human', 'ai') and content.
            Must follow the LangChain `BaseMessage` structure.

    Example:
        {
            "messages": [
                { "type": "human", "content": "Hi, what can you do?" },
                { "type": "ai", "content": "I can help you understand parsing rules." }
            ]
        }
    """
    messages: List[ChatRequestMessage]


class ChatResponse(BaseModel):
    """
    Schema representing a chat response to the frontend
    Attributes:
        type (ChatRole): Type of the message.
        content (str): The generated content from the AI agent, \
            typically a text response to the user's query.
    """
    type: ChatRole = ChatRole.AI
    content: str

    class Config:
        """Config class for mapping"""
        from_attributes=True
