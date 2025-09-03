"""
This module defines the ClientScope enumeration,
representing various access scopes for clients.
"""

from enum import Enum


class ClientScope(Enum):
    """
    ClientScope is an enumeration of access scopes available to clients.

    Attributes:
        DOCUMENT_READ: Permission to read documents.
        DOCUMENT_WRITE: Permission to write documents.
        DOCUMENT_DELETE: Permission to delete documents.

        COLLECTION_READ: Permission to read collections.
        COLLECTION_WRITE: Permission to write collections.
        COLLECTION_DELETE: Permission to delete collections.

        CATEGORY_READ: Permission to read categories.
        CATEGORY_WRITE: Permission to write categories.

        CHAT_SESSION_READ: Permission to read chat sessions.
        CHAT_SESSION_WRITE: Permission to write chat sessions.

        CHAT: Permission to access chat functionality

        SYNC: Permission to perform synchronization operations.
    """
    # Documents
    DOCUMENT_READ = "document:read"
    DOCUMENT_WRITE = "document:write"
    DOCUMENT_DELETE = "document:delete"

    # Collections
    COLLECTION_READ = "collection:read"
    COLLECTION_WRITE = "collection:write"
    COLLECTION_DELETE = "collection:delete"

    # Categories
    CATEGORY_READ = "category:read"
    CATEGORY_WRITE = "category:write"
    CATEGORY_DELETE = "category:delete"

    # Chat session
    CHAT_SESSION_WRITE = "chat_session:write"
    CHAT_SESSION_READ = "chat_session:read"
    CHAT_SESSION_DELETE = "chat_session:delete"

    # External user
    EXTERNAL_USER_READ = "external_user:read"
    EXTERNAL_USER_WRITE = "external_user:write"
    EXTERNAL_USER_DELETE = "external_user:delete"

    # Chat
    CHAT = "chat"

    # Sync data
    SYNC = "sync"
