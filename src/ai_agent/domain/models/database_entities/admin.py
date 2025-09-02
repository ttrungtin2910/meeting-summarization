"""
Admin Model Module
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Admin(BaseModel):
    """
    Represents an administrator of the platform.

    Attributes:
        id (UUID): Unique identifier for the admin
        email (str): Email of the admin
        hashed_password (str): The hashed password for the admin.
        created_at (datetime): Timestamp when the admin was created
    """
    id: UUID
    email: str
    hashed_password: str
    created_at: datetime

    class Config:
        """Config to map data"""
        from_attributes = True
