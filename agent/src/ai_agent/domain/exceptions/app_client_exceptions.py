"""
Custom exceptions related to AppClient.
"""


from typing import Optional
from uuid import UUID


class AppClientNotFound(Exception):
    """
    Exception raised when attempting to access an AppClient that does not exist.
    """

    def __init__(
            self,
            client_id: Optional[UUID] = None,
            client_name: Optional[str] = None):
        if client_id:
            self.message = f"AppClient with ID '{client_id}' not found"
        if client_name:
            self.message = f"AppClient with name '{client_name}' not found"
        else:
            self.message = "AppClient not found"
        super().__init__(self.message)


class AppClientAlreadyExists(Exception):
    """
    Exception raised when attempting to create an AppClient with a duplicate name
        in a specific organization.
    """

    def __init__(self, client_name):
        self.client_name = client_name
        self.message = f"AppClient with name '{self.client_name}' already exists"
        super().__init__(self.message)


class AppClientInvalidScope(Exception):
    """
    Exception raised when an AppClient is assigned an invalid scope.
    """

    def __init__(self, scope_name):
        self.scope_name = scope_name
        self.message = f"Scope '{self.scope_name}' is not valid for this client"
        super().__init__(self.message)
