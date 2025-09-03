"""
Download information module.

This module provides a schema for representing information about downloadable files
"""

from datetime import datetime

from pydantic import BaseModel


class DownloadInfoDTO(BaseModel):
    """
    Schema for download information of a file.

    This class defines the structure for representing downloadable file information,
    particularly for temporary or signed URLs that may expire after a certain time.

    Attributes:
        name (str): The name of the file being downloaded
        url (str): The URL where the file can be downloaded from
        expires_at (datetime): The timestamp when the download URL will expire
    """
    name: str
    url: str
    expires_at: datetime
