"""
This module defines the association table for app clients and collections.
"""

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID

from ai_agent.infrastructure.database.base.base_model import Base

app_client_collection_model = Table(
    "app_client_collection",
    Base.metadata,
    Column(
        "app_client_id",
        UUID(as_uuid=True),
        ForeignKey("app_clients.client_id"),
        primary_key=True
    ),
    Column(
        "collection_id",
        UUID(as_uuid=True),
        ForeignKey("collections.id"),
        primary_key=True
    ),
)
