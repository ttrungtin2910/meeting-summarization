"""
This module defines the AdminContext model,
representing the current authenticated admin within the system.
"""

from uuid import UUID

from pydantic import BaseModel


class AdminContext(BaseModel):
    """
    Model representing the current authenticated admin.

    Attributes:
        admin_id: UUID of the admin
    """
    admin_id: UUID
