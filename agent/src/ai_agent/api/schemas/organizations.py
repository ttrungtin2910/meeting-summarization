"""
Organization Schema Module
"""

import re
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class OrganizationCreate(BaseModel):
    """
    Schema for creating a new organization via API.

    This model validates incoming data when creating a new organization,
    ensuring that required fields are present and properly formatted.

    Attributes:
        name (str): Name of the organization
    """
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Name of the organization"
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=64
    )

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, value):
        """
        Ensure the password has minimum strength.

        Must contain at least:
        - one uppercase letter
        - one lowercase letter
        - one digit
        - one special character
        """
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r"[0-9]", value):
            raise ValueError("Password must contain at least one digit.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Password must contain at least one special character.")
        return value


class OrganizationUpdate(BaseModel):
    """
    Schema for updating an existing organization via API.

    This model validates incoming data when updating an organization,
    ensuring that fields are properly formatted.

    Attributes:
        name (str): Updated name of the organization
    """
    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="Updated name of the organization"
    )

    password: Optional[str] = Field(
        None,
        min_length=8,
        max_length=64
    )

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, value):
        """
        Ensure the password has minimum strength.

        Must contain at least:
        - one uppercase letter
        - one lowercase letter
        - one digit
        - one special character
        """
        if value is None:
            return value
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r"[0-9]", value):
            raise ValueError("Password must contain at least one digit.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Password must contain at least one special character.")
        return value
