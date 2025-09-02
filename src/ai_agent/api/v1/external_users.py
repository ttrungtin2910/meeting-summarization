"""
API endpoints for managing external users.

Includes routes to get a single external user, list users, and delete users.
All actions are scoped to the authenticated client and organization.
"""

from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status

from ai_agent.api.dependencies.security_dependencies import \
    get_current_organization
from ai_agent.api.dependencies.service_dependencies.external_user_service_dependencies import \
    get_external_user_service
from ai_agent.application.services.database_services import ExternalUserService
from ai_agent.domain.exceptions.auth_exceptions import InsufficientScope
from ai_agent.domain.exceptions.external_user_exceptions import \
    ExternalUserNotFound
from ai_agent.domain.models.database_entities.external_user import ExternalUser
from ai_agent.domain.models.security_contexts.organization_context import \
    OrganizationContext

router = APIRouter()


@router.get(
    "/external-users/{external_user_id}",
    response_model=ExternalUser,
)
def get_external_user(
    external_user_id: UUID,
    service: ExternalUserService = Depends(get_external_user_service),
    organization_context: OrganizationContext = Depends(get_current_organization),
):
    """
    Retrieve a specific external user by their external ID.

    Args:
        external_user_id (UUID): ID of the external user in the organization.

    Returns:
        ExternalUser: The matched external user.

    Raises:
        404: If the specified external user is not found
        403: If the client does not have the required scope.
    """
    try:
        return service.get_external_user(
            external_user_id=external_user_id,
            organization_context=organization_context
        )
    except ExternalUserNotFound as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exception)
        ) from exception
    except InsufficientScope as exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exception)
        ) from exception


@router.get(
    "/external-users",
    response_model=List[ExternalUser],
)
def list_external_users(
    service: ExternalUserService = Depends(get_external_user_service),
    organization_context: OrganizationContext = Depends(get_current_organization),
):
    """
    List all external users belonging to the current organization.

    Returns:
        List[ExternalUser]: All external users for this organization.

    Raises:
        403: If the client does not have the required scope.
    """
    try:
        return service.list_external_users(organization_context=organization_context)
    except InsufficientScope as exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exception)
        ) from exception


@router.delete(
    "/external-users/{external_user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_external_user(
    external_user_id: UUID,
    service: ExternalUserService = Depends(get_external_user_service),
    organization_context: OrganizationContext = Depends(get_current_organization),
):
    """
    Delete an external user by their external ID.

    Args:
        external_user_id (UUID): ID of the external user in the organization.
        current_client (CurrentClient): The authenticated client.

    Raises:
        404: If the specified external user is not found
        403: If the client does not have the required scope.
    """
    try:
        service.delete_external_user(
            external_user_id=external_user_id,
            organization_context=organization_context
        )
    except ExternalUserNotFound as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exception)
        ) from exception
    except InsufficientScope as exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exception)
        ) from exception
