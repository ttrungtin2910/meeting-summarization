"""
External User Model Module
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ExternalUser(BaseModel):
    """
    ExternalUser data model.

    Attributes:
        id (UUID): Internal UUID of the external user record.
        external_user (str): The ID assigned to this user by the external system.
        organization_id (UUID): The organization that owns this user.
        created_at (datetime): Timestamp of when the external user was created.
    """

    id: UUID
    external_user: str
    organization_id: UUID
    created_at: datetime

    class Config:
        """Enable ORM mode for mapping from SQLAlchemy models."""
        from_attributes = True
