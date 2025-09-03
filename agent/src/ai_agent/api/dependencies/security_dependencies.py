"""
This module provides functionality to authenticate
and retrieve the current client using JWT.
"""

from typing import Dict
from uuid import UUID

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from ai_agent.api.dependencies.token_manager_dependencies import \
    get_token_manager
from ai_agent.domain.models.security_contexts.admin_context import AdminContext
from ai_agent.domain.models.security_contexts.client_context import \
    ClientContext
from ai_agent.domain.models.security_contexts.organization_context import \
    OrganizationContext
from ai_agent.infrastructure.token_manager.base_token_manager import \
    BaseTokenManager

security_scheme = HTTPBearer()


def get_current_client(
    credentials: HTTPAuthorizationCredentials = Security(security_scheme),
    token_manager: BaseTokenManager = Depends(get_token_manager)
) -> ClientContext:
    """
    Retrieves the current authenticated client using the provided JWT
    credentials.

    Args:
        credentials (HTTPAuthorizationCredentials): The security credentials
            containing the JWT token
        token_manager (BaseTokenManager): The manager used to create and verify the JWT token

    Returns:
        ClientContext: An instance representing the authenticated client,
        including client ID, organization ID.

    Raises:
        HTTPException:
            - 401 Unauthorized: If the token is invalid or expired.
            - 401 Unauthorized: If the token payload is malformed.
    """
    token: str = credentials.credentials
    payload: Dict = token_manager.decode(token)

    # If malformed or expired token, verify_token will return None
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    try:
        return ClientContext(
            client_id=UUID(payload["client_id"]),
            organization_id=UUID(payload["organization_id"]),
            collection_ids=[
                UUID(collection_id) for collection_id in payload.get("collection_ids", [])
            ]
        )
    except Exception as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Malformed token payload"
        ) from exception


def get_current_organization(
    credentials: HTTPAuthorizationCredentials = Security(security_scheme),
    token_manager: BaseTokenManager = Depends(get_token_manager)
) -> OrganizationContext:
    """
    Authenticates and retrieves the current organization.

    Args:
        credentials (HTTPBearer): JWT token credentials.
        token_manager (BaseTokenManager): The manager used to create and verify the JWT token

    Returns:
        OrganizationContext: Authenticated organization instance.

    Raises:
        HTTPException: 401 Unauthorized for invalid or malformed token.
    """
    try:
        token = credentials.credentials
        payload = token_manager.decode(token)
        if not payload:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
        return OrganizationContext(
            organization_id=payload["organization_id"]
        )

    except Exception as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Malformed token payload"
        ) from exception


def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Security(security_scheme),
    token_manager: BaseTokenManager = Depends(get_token_manager)
) -> AdminContext:
    """
    Authenticates and retrieves the current admin.

    Args:
        credentials (HTTPBearer): JWT token credentials.
        token_manager (BaseTokenManager): The manager used to create and verify the JWT token

    Returns:
        AdminContext: Authenticated admin instance.

    Raises:
        HTTPException: 401 Unauthorized for invalid or malformed token.
    """
    try:
        token = credentials.credentials
        payload = token_manager.decode(token)
        if not payload:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
        return AdminContext(
            admin_id=payload.get("admin_id")
        )

    except Exception as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Malformed token payload"
        ) from exception
