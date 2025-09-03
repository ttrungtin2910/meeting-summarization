"""
Domain model for Organization, used across application layers.

This module defines the core domain entity for organizations
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Organization(BaseModel):
    """
    Domain entity representing an organization.

    Attributes:
        id (UUID): The unique identifier for the organization
        name (str): The display name of the organization
        hashed_password (str): Hashed password
        is_active (bool): Whether the organization is active or not.
        created_at (datetime): The timestamp when the organization was created
    """
    id: UUID

    name: str
    hashed_password: str

    is_active: bool
    created_at: datetime

    class Config:
        """Config to map data"""
        from_attributes = True
