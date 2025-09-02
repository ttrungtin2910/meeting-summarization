"""
This module defines the ClientContext model,
representing the current authenticated client within the system.
"""

from typing import List
from uuid import UUID

from pydantic import BaseModel


class ClientContext(BaseModel):
    """
    Model representing the current authenticated client.

    Attributes:
        client_id: A UUID representing the unique identifier of the client.
        organization_id: A UUID representing the unique identifier
            of the organization to which the client belongs.
        collection_ids (List[UUID]): A list of UUIDs representing the collection IDs
    """
    client_id: UUID
    organization_id: UUID
    collection_ids: List[UUID]
