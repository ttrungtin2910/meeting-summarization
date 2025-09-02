"""
URL Utility module

This module provides utilities for working with URL
"""

import os
import urllib.parse
import uuid
from uuid import UUID


def create_connection_url(config):
    """
    Method to create connection URL from config.

    Args:
        config: Configuration object containing required attributes:
            - password (str): Password of the database
            - provider (str): database provider. E.g. postgres
            - driver (str): driver to work with the database
            - user (str): Username
            - host (str): Host of the database
            - port (str): Port of the database
            - database (str): Name of the database

    Returns:
        str: Connection URL
    """
    encoded_password = urllib.parse.quote_plus(config.password)
    connection_url = (
        f"{config.provider}+{config.driver}://"
        f"{config.user}:{encoded_password}"
        f"@{config.host}:{config.port}/{config.database}"
    )
    return connection_url


def build_remote_path(
        original_filename: str,
        collection_id: UUID,
        category_id: UUID,
        organization_id: UUID
    ) -> str:
    """
    Build a unique remote path for storing a file

    Args:
        original_filename (str): Name of uploaded file (may be non-unique).
        collection_id (UUID): The collection this file belongs to.
        category_id (UUID): The category this file belongs to.
        organization_id (UUID): ID of the organization

    Returns:
        str: Path to be used.
    """
    filename = os.path.basename(original_filename)
    unique_prefix = str(uuid.uuid4())
    return f"agents/{organization_id}/{collection_id}/{category_id}/{unique_prefix}_{filename}"


def add_extension(display_name: str, filename: str) -> str:
    """
    Ensure the given display_name ends with the extension from filename.

    Args:
        display_name (str): The name provided by user.
        filename (str): The original filename with extension (e.g. file.pdf).

    Returns:
        str: Safe name with proper extension.
    """
    _, ext = os.path.splitext(filename)
    if not display_name.lower().endswith(ext.lower()):
        display_name += ext
    return display_name
