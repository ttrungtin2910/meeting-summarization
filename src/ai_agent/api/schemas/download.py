"""
schemas for download
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class DownloadResponse(BaseModel):
    """
    Schema for download information of a file.

    This class defines the structure for representing downloadable file information,
    particularly for temporary or signed URLs that may expire after a certain time.

    Attributes:
        id (UUID): ID of the document
        name (str): The name of the file being downloaded
        url (str): The URL where the file can be downloaded from
        expires_at (datetime): The timestamp when the download URL will expire
    """
    id: UUID
    name: str
    url: str
    expires_at: datetime

    class Config:
        """configuration for ORM mode"""
        from_attributes = True
