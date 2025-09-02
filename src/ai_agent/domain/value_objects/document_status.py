"""
Enum definitions for Document status.
"""

from enum import Enum


class DocumentStatus(Enum):
    """
    Enumeration representing the status of a document in the system.

    Attributes:
        PENDING: The document has been uploaded but not yet processed.
        EMBEDDED: The document has been embedded into the vector database.
        DELETED: The document has been marked for deletion.
        UPDATED: The document has been modified after the initial upload.
    """
    PENDING = "pending"
    EMBEDDED = "embedded"
    DELETED = "deleted"
    UPDATED = "updated"
