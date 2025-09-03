"""
Custom exceptions related to external user.
"""


class ExternalUserNotFound(Exception):
    """
    Exception raised when attempting to access an External user that does not exist.
    """
    def __init__(self):
        self.message = "External user not found"
        super().__init__(self.message)
