"""
Custom exceptions related to Chat logic.
"""


class MessageNotFound(Exception):
    """
    Exception raised when attempting to get a message that is not found.
    """

    def __init__(self):
        self.message = "message not found"
        super().__init__(self.message)
