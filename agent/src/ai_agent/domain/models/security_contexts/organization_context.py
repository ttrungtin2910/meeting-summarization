"""
This module defines the OrganizationContext model,
representing the current authenticated organization within the system.
"""

from uuid import UUID

from pydantic import BaseModel


class OrganizationContext(BaseModel):
    """
    Model representing the current authenticated organization.

    Attributes:
        organization_id: A UUID representing the unique identifier
            of the organization to which the client belongs.
    """
    organization_id: UUID
