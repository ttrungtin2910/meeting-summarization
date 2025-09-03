"""
Custom exceptions related to Document domain logic.
"""

from uuid import UUID


class DocumentNotFound(Exception):
    """
    Exception raised when attempting to get a document with an id that does not exist.

    Attributes:
        document_id (UUID): The document id that caused the exception
        message (str): Descriptive error message
    """
    def __init__(self, document_id: UUID):
        self.document_id = document_id
        self.message = f"document with ID '{self.document_id}' does not exist"
        super().__init__(self.message)


class DocumentDeleted(Exception):
    """
    Exception raised when attempting to delete a document that already has deleted status.

    Attributes:
        document_id (UUID): The document id that caused the exception
        message (str): Descriptive error message
    """
    def __init__(self, document_id: UUID):
        self.document_id = document_id
        self.message = f"document with ID '{self.document_id}' already in deleted state"
        super().__init__(self.message)
