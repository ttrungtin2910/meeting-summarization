"""
Organization data transfer objects (DTOs) module.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class OrganizationCreateRequestDTO(BaseModel):
    """
    DTO for creating a new organization, from API to service

    This class defines the structure for data required when creating
    a new organization

    Attributes:
        name (str): The name of the organization to create
        password (str): The password for the organization
    """
    name: str
    password: str

    class Config:
        """ Config for mapping data"""
        from_attributes = True


class OrganizationCreateDTO(BaseModel):
    """
    DTO for creating a new organization.

    This class defines the structure for data required when creating
    a new organization

    Attributes:
        name (str): The name of the organization to create
        hashed_password (str): The hashed password for the organization
        created_at (datetime): timestamp of organization creation
    """
    name: str
    hashed_password: str
    created_at: datetime


class OrganizationUpdateRequestDTO(BaseModel):
    """
    DTO for updating an existing organization from API to application.

    This class defines the structure for data allowed to be modified
    when updating an organization

    Attributes:
        name (Optional[str]): The new name for the organization
        password (Optional[str]): The new password for the organization
    """
    name: Optional[str] = None
    password: Optional[str] = None

    class Config:
        """ Config for mapping data"""
        from_attributes = True


class OrganizationUpdateDTO(BaseModel):
    """
    DTO for updating an existing organization.

    This class defines the structure for data allowed to be modified
    when updating an organization

    Attributes:
        name (Optional[str]): The new name for the organization
        hashed_password (Optional[str]): The hashed new password for the organization
    """
    name: Optional[str] = None
    hashed_password: Optional[str] = None

    class Config:
        """ Config for mapping data"""
        from_attributes = True


class OrganizationResponse(BaseModel):
    """
    DTO for organization responses from the API.

    This class defines the structure of organization data returned
    in API responses.

    Attributes:
        id (UUID): The unique identifier of the organization
        name (str): The name of the organization
        is_active (bool): Whether the organization is active or not.
        created_at (datetime): The timestamp when the organization was created
    """
    id: UUID
    name: str
    is_active: bool
    created_at: datetime

    class Config:
        """
        Pydantic configuration for the OrganizationResponse model.
        """
        from_attributes = True
