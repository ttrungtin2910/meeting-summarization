"""
Custom exceptions related to Collection domain logic.
"""


from typing import Optional
from uuid import UUID


class CollectionAlreadyExists(Exception):
    """
    Exception raised when attempting to create a collection with a name that already exists.

    Attributes:
        name (str): The duplicate collection name that caused the exception
        message (str): Descriptive error message
    """
    def __init__(self, name: str):
        self.name = name
        self.message = f"collection with name '{self.name}' already exists"
        super().__init__(self.message)


class CollectionNotFound(Exception):
    """
    Exception raised when attempting to get a collection with a id that does not exist.

    Attributes:
        message (str): Descriptive error message
    """
    def __init__(self, collection_id: Optional[UUID]):
        if collection_id:
            self.message = f"collection with ID '{collection_id}' does not exist"
        else:
            self.message = "collection not found"
        super().__init__(self.message)


class CollectionInUseError(Exception):
    """
    Raised when attempting to delete a collection that still has associated categories.
    """
    def __init__(self, collection_id: UUID):
        self.collection_id = collection_id
        super().__init__(f"Collection '{collection_id}' cannot be deleted \
because it has associated categories.")


class DefaultCollectionNotFound(Exception):
    """
    Exception raised when the default collection for a specific organization does not exist.

    Attributes:
        organization_id (UUID): The organization ID that caused the exception.
        message (str): Descriptive error message.
    """

    def __init__(self, organization_id: UUID):
        self.organization_id = organization_id
        self.message = f"Default collection for organization with ID '{self.organization_id}' does not exist."
        super().__init__(self.message)
