"""
Auth API schemas.

This module defines the models for auth API request and response validation.
"""

from uuid import UUID

from pydantic import BaseModel


class AdminLoginRequest(BaseModel):
    """
    Represents the data required for an admin to login

    Attributes:
        email (str): Email of the admin
        password (str): Password of the admin
    """
    email: str
    password: str


class OrganizationLoginRequest(BaseModel):
    """
    OrganizationLoginRequest represents the data required for an organization to login

    Attributes:
        name (str): Name of the organization
        password (str): Password of the organization
    """
    name: str
    password: str


class ClientLoginRequest(BaseModel):
    """
    ClientLoginRequest represents the data required to request an access token for a client.

    Attributes:
        client_id: An UUID representing the unique identifier of the client.
        client_secret: A string representing the secret key associated with the client.
    """
    client_id: UUID
    client_secret: str

class TokenResponse(BaseModel):
    """
    TokenResponse represents the data returned after a successful token request.

    Attributes:
        access_token: A string representing the access token issued to the client.
        token_type: A string representing the type of the token, defaulting to "bearer".
    """
    access_token: str
    token_type: str = "bearer"
