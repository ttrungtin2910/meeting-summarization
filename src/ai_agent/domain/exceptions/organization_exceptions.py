"""
Custom exceptions related to Organization.
"""


from typing import Optional
from uuid import UUID


class OrganizationNotFound(Exception):
    """
    Exception raised when attempting to get an organization that is not found.
    """

    def __init__(self):
        self.message = "Access denied or organization not found."
        super().__init__(self.message)


class OrganizationAlreadyExists(Exception):
    """
    Exception raised when attempting to create an organization that already exists.
    """

    def __init__(self, organization_name):
        self.organization_name = organization_name
        self.message = f"organization with name '{self.organization_name}' already exists"
        super().__init__(self.message)


class OrganizationInUse(Exception):
    """
    Exception raised when attempting to delete an organization that still has associated collections
    """

    def __init__(self, organization_id: Optional[UUID]):
        if organization_id:
            self.message = f"Organization '{organization_id}' cannot be deleted \
because it has associated collections."
        else:
            self.message = "The organization is in use"
        super().__init__(self.message)
