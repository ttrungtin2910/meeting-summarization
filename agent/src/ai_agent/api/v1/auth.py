"""
Authentication endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status

from ai_agent.api.dependencies.service_dependencies.auth_service_dependencies import \
    get_auth_service
from ai_agent.api.schemas.auth import (AdminLoginRequest, ClientLoginRequest,
                                       OrganizationLoginRequest, TokenResponse)
from ai_agent.application.services.auth_service import AuthService
from ai_agent.domain.exceptions.auth_exceptions import InvalidCredentials

router = APIRouter()


@router.post("/auth/app-client", response_model=TokenResponse)
def login_app_client(
    request: ClientLoginRequest,
    service: AuthService = Depends(get_auth_service),
):
    """
    Generate an access token for an application client.

    The token includes:
        - client_id: Identifier of the calling client.
        - organization_id: The organization to which the client belongs.
        - exp: Expiration time.

    Args:
        request (TokenRequest):
            Contains the client_id (UUID) and client_secret (string) for authentication.

    Returns:
        TokenResponse:
            A JSON object containing the JWT access_token and its type ("bearer").

    Raises:
        401: If the provided client credentials are invalid or the client is inactive.
    """
    try:
        token = service.login_client(
            client_id=request.client_id,
            client_secret=request.client_secret
        )
        return TokenResponse(access_token=token)
    except InvalidCredentials as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exception)
        ) from exception


@router.post("/auth/organization", response_model=TokenResponse)
def login_organization(
    request: OrganizationLoginRequest,
    service: AuthService = Depends(get_auth_service),
):
    """
    Handles organization login and returns an access token.

    Args:
        request (OrganizationLoginRequest): The login request containing
            the organization's name and password.

    Returns:
        TokenResponse: Contains the JWT access token upon successful login.

    Raises:
        HTTPException: 401 Unauthorized if credentials are invalid.
    """
    try:
        token = service.login_organization(
            name=request.name,
            password=request.password
        )
        return TokenResponse(access_token=token)

    except InvalidCredentials as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exception)
        ) from exception


@router.post("/auth/admin", response_model=TokenResponse)
def login_admin(
    request: AdminLoginRequest,
    service: AuthService = Depends(get_auth_service),
):
    """
    Handles admin login and returns an access token.

    Args:
        request (AdminLoginRequest): The login request containing
            the admin's email and password.

    Returns:
        TokenResponse: Contains the JWT access token upon successful login.

    Raises:
        HTTPException: 401 Unauthorized if credentials are invalid.
    """
    try:
        token = service.login_admin(
            email=request.email,
            password=request.password
        )
        return TokenResponse(access_token=token)

    except InvalidCredentials as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exception)
        ) from exception
