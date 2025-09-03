"""
Custom exceptions related to Authorization or authentication.
"""


class InvalidCredentials(Exception):
    """
    Exception raised for errors in authentication due to invalid credentials.

    Attributes:
        message: Explanation of the error.
    """
    def __init__(self):
        self.message = "Unauthorized"
        super().__init__(self.message)


class InsufficientScope(Exception):
    """
    Exception raised for errors when trying to access an API
        that is out of scope of the client.

    Attributes:
        message: Explanation of the error.
    """
    def __init__(self, scope):
        self.message = f"Insufficient scope: {scope}"
        super().__init__(self.message)
