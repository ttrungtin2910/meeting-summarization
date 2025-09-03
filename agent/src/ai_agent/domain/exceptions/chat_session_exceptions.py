"""
Custom exceptions related to chat session domain logic.
"""

from uuid import UUID


class ChatSessionNotFound(Exception):
    """
    Exception raised when attempting to get a chat session with an id that does not exist.

    Attributes:
        chat_session_id (UUID): The chat session id that caused the exception
        message (str): Descriptive error message
    """
    def __init__(self, chat_session_id: UUID):
        self.chat_session_id = chat_session_id
        self.message = f"chat session with ID '{self.chat_session_id}' does not exist"
        super().__init__(self.message)
