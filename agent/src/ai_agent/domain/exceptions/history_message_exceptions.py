"""
Custom exceptions for HistoryMessage operations.
"""

from uuid import UUID


class HistoryMessageNotFound(Exception):
    """
    Raised when a history message with the specified ID is not found.
    """

    def __init__(self, message_id: UUID):
        """
        Initialize HistoryMessageNotFound exception.

        Args:
            message_id (UUID): The ID of the missing history message.
        """
        self.message_id = message_id
        super().__init__(f"History message with ID {message_id} was not found.")
