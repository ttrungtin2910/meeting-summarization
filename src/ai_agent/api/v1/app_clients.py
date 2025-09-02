"""
Admin API routes for managing AppClients.
"""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, status

from ai_agent.api.dependencies.security_dependencies import \
    get_current_organization
from ai_agent.api.dependencies.service_dependencies.app_client_service_dependencies import \
    get_app_client_service
from ai_agent.api.schemas.app_clients import (AppClientCreateRequest,
                                              AppClientCreateResponse,
                                              AppClientResponse,
                                              AppClientUpdate)
from ai_agent.application.services.database_services import AppClientService
from ai_agent.domain.dtos.app_client_dto import (AppClientCreateRequestDTO,
                                                 AppClientUpdateDTO)
from ai_agent.domain.exceptions.app_client_exceptions import (
    AppClientAlreadyExists, AppClientNotFound)
from ai_agent.domain.exceptions.collection_exceptions import CollectionNotFound
from ai_agent.domain.exceptions.organization_exceptions import \
    OrganizationNotFound
from ai_agent.domain.models.database_entities.app_client import AppClient
from ai_agent.domain.models.security_contexts.organization_context import \
    OrganizationContext


# Define router
router = APIRouter()


@router.get("/app-clients", response_model=List[AppClientResponse])
def list_app_clients(
    service: AppClientService = Depends(get_app_client_service),
    organization_context: OrganizationContext = Depends(get_current_organization)
):
    """
    List all AppClients in an organization.

    Returns:
        List[AppClient]: All clients of the organization.

    Raises:
        403: If the organization is invalid or inaccessible.
    """
    try:
        app_clients = service.list_app_clients(organization_context)
        return [
            AppClientResponse.model_validate(app_client) for app_client in app_clients
        ]
    except OrganizationNotFound as exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exception)
        ) from exception


@router.get("/app-clients/{client_id}", response_model=AppClientResponse)
def get_app_client(
    client_id: UUID,
    service: AppClientService = Depends(get_app_client_service),
    organization_context: OrganizationContext = Depends(get_current_organization)
):
    """
    Get a single AppClient by ID.

    Args:
        client_id (UUID): ID of the app client.

    Returns:
        AppClient: The requested app client.

    Raises:
        403: If the organization is invalid.
        404: If the client does not exist.
    """
    try:
        app_client: AppClient = service.get_by_id(client_id, organization_context)
        return AppClientResponse.model_validate(app_client)

    except OrganizationNotFound as exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exception)
        ) from exception
    except AppClientNotFound as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exception)
        ) from exception


@router.post(
        "/app-clients",
        response_model=AppClientCreateResponse,
        status_code=status.HTTP_201_CREATED
    )
def create_app_client(
    request: AppClientCreateRequest,
    service: AppClientService = Depends(get_app_client_service),
    organization_context: OrganizationContext = Depends(get_current_organization)
):
    """
    Create a new AppClient.

    Args:
        request (AppClientCreateRequestDTO): Data for new app client.

    Returns:
        AppClient: Created app client.

    Raises:
        403: If the organization is invalid.
        409: If the client name already exists or collection not found
    """
    try:
        create_dto = AppClientCreateRequestDTO.model_validate(request)
        result = service.create_app_client(create_dto, organization_context)
        return AppClientCreateResponse.model_validate(result)

    except OrganizationNotFound as exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exception)
        ) from exception

    except AppClientAlreadyExists as exception:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exception)
        ) from exception

    except CollectionNotFound as exception:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exception)
        ) from exception


@router.patch("/app-clients/{client_id}", response_model=AppClientResponse)
def update_app_client(
    client_id: UUID,
    request: AppClientUpdate,
    service: AppClientService = Depends(get_app_client_service),
    organization_context: OrganizationContext = Depends(get_current_organization)
):
    """
    Update an existing AppClient.

    Args:
        client_id (UUID): ID of the app client.
        request (AppClientUpdate): Fields to update.

    Returns:
        AppClient: Updated client.

    Raises:
        403: If organization is invalid.
        404: If app client or collection_ids not found.
        409: If new name already exists.
    """
    try:
        update_dto: AppClientUpdateDTO = AppClientUpdateDTO.model_validate(request)
        result = service.update_app_client(client_id, organization_context, update_dto)
        return AppClientResponse.model_validate(result)

    except OrganizationNotFound as exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exception)
        ) from exception
    except AppClientNotFound as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exception)
        ) from exception
    except AppClientAlreadyExists as exception:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exception)
        ) from exception
    except CollectionNotFound as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exception)
        ) from exception

@router.delete("/admin/app-clients/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_app_client(
    client_id: UUID,
    service: AppClientService = Depends(get_app_client_service),
    organization_context: OrganizationContext = Depends(get_current_organization)
):
    """
    Delete an AppClient.

    Args:
        client_id (UUID): ID of the app client.

    Returns:
        None

    Raises:
        403: If organization is invalid.
        404: If client not found.
    """
    try:
        service.delete_app_client(client_id, organization_context)
    except OrganizationNotFound as exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exception)
        ) from exception
    except AppClientNotFound as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exception)
        ) from exception


@router.post("/app-clients/{client_id}/activate", response_model=AppClientResponse)
def activate_app_client(
    client_id: UUID = Path(...),
    organization_context: OrganizationContext = Depends(get_current_organization),
    service: AppClientService = Depends(get_app_client_service)
):
    """
    Activate an AppClient (set is_active=True).

    Args:
        client_id (UUID): AppClient ID.

    Returns:
        AppClientResponse: Updated app client.

    Raises:
        403: If organization invalid.
        404: If client not found.
    """
    try:
        dto = AppClientUpdateDTO(is_active=True)
        result = service.update_app_client(client_id, organization_context, dto)
        return AppClientResponse.model_validate(result)

    except OrganizationNotFound as exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exception)
        ) from exception
    except AppClientNotFound as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exception)
        ) from exception


@router.post("/app-clients/{client_id}/deactivate", response_model=AppClientResponse)
def deactivate_app_client(
    client_id: UUID = Path(...),
    organization_context: OrganizationContext = Depends(get_current_organization),
    service: AppClientService = Depends(get_app_client_service)
):
    """
    Deactivate an AppClient (set is_active=False).

    Args:
        client_id (UUID): AppClient ID.

    Returns:
        AppClientResponse: Updated app client.

    Raises:
        403: If organization invalid.
        404: If client not found.
    """
    try:
        dto = AppClientUpdateDTO(is_active=False)
        result = service.update_app_client(client_id, organization_context, dto)
        return AppClientResponse.model_validate(result)

    except OrganizationNotFound as exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exception)
        ) from exception
    except AppClientNotFound as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exception)
        ) from exception
