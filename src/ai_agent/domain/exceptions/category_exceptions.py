"""
Custom exceptions related to Category domain logic.
"""

from uuid import UUID


class CategoryAlreadyExists(Exception):
    """
    Exception raised when attempting to create a category with a name that already exists.

    Attributes:
        name (str): The duplicate collection name that caused the exception
        collection_id (UUID): ID of the collection of the category that caused the exception
        message (str): Descriptive error message
    """
    def __init__(self, name: str, collection_id: UUID):
        self.name = name
        self.collection_id = collection_id
        self.message = f"category with name '{self.name}' already exists \
in collection '{self.collection_id}'"
        super().__init__(self.message)


class CategoryNotFound(Exception):
    """
    Exception raised when attempting to get a category with a id that does not exist.

    Attributes:
        category_id (UUID): The category id that caused the exception
        message (str): Descriptive error message
    """
    def __init__(self, category_id: UUID):
        self.category_id = category_id
        self.message = f"category with ID '{self.category_id}' does not exist"
        super().__init__(self.message)


class CategoryInUseError(Exception):
    """
    Raised when attempting to delete a category that still has associated documents.
    """
    def __init__(self, category_id: UUID):
        self.category_id = category_id
        super().__init__(f"Category '{category_id}' cannot be deleted \
because it has associated documents or deleted documents are not synchronized.")
