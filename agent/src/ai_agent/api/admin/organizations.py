"""
Organizations API Module

This module provides endpoints for managing organizations in the AI Agent system.
It includes functionality for creating, retrieving, updating, and deleting organizations.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from ai_agent.api.dependencies.security_dependencies import get_current_admin
from ai_agent.api.dependencies.service_dependencies.organization_service_dependencies import \
    get_organization_service
from ai_agent.api.schemas.organizations import (OrganizationCreate,
                                                OrganizationUpdate)
from ai_agent.application.services.database_services.organization_service import \
    OrganizationService
from ai_agent.domain.dtos.organization_dto import (
    OrganizationCreateRequestDTO, OrganizationResponse, OrganizationUpdateRequestDTO)
from ai_agent.domain.exceptions.organization_exceptions import (
    OrganizationAlreadyExists, OrganizationInUse, OrganizationNotFound)
from ai_agent.domain.models.security_contexts.admin_context import AdminContext

router = APIRouter(prefix="/organizations")


@router.post("", response_model=OrganizationResponse)
def create_organization(
    request: OrganizationCreate,
    _: AdminContext = Depends(get_current_admin),
    service: OrganizationService = Depends(get_organization_service),
):
    """
    Create a new organization.

    This endpoint allows creating a new organization with the provided details.

    Args:
        request (OrganizationCreate): The organization data to create.

    Returns:
        OrganizationResponse: The created organization details.

    Raises:
        409: if an organization with the same identifier already exists,
            or organization's name is empty
    """
    try:
        data = OrganizationCreateRequestDTO.model_validate(request)
        organization = service.create_organization(
            data,
        )
        return OrganizationResponse.model_validate(organization)

    except (OrganizationAlreadyExists, ValueError) as exception:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exception)
        ) from exception


@router.get("", response_model=list[OrganizationResponse])
def list_organizations(
    _: AdminContext = Depends(get_current_admin),
    service: OrganizationService = Depends(get_organization_service),
):
    """
    Retrieve a list of all organizations.

    This endpoint fetches all organizations from the system and returns them
    as a list of organization objects.

    Args:
        None

    Returns:
        list[OrganizationResponse]: A list of organization objects, each converted
        to the OrganizationResponse model.

    Example:
        GET /organizations
    """
    results = service.get_list_organizations()
    return [OrganizationResponse.model_validate(result) for result in results]


@router.get("/{organization_id}", response_model=OrganizationResponse)
def get_organization(
    organization_id: UUID,
    _: AdminContext = Depends(get_current_admin),
    service: OrganizationService = Depends(get_organization_service),
):
    """
    Get details of a specific organization by ID.

    Parameters:
    - organization_id: UUID of the organization to retrieve

    Returns:
    - OrganizationResponse: Details of the requested organization

    Raises:
    - 404: Organization not found
    """
    try:
        result = service.get_organization(
            organization_id,
        )
        return OrganizationResponse.model_validate(result)
    except OrganizationNotFound as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exception)
        ) from exception


@router.patch("/{organization_id}", response_model=OrganizationResponse)
def update_organization(
    organization_id: UUID,
    request: OrganizationUpdate,
    _: AdminContext = Depends(get_current_admin),
    service: OrganizationService = Depends(get_organization_service),
):
    """
    Update an existing organization.

    Parameters:
    - organization_id: UUID of the organization to update
    - request: Organization update data

    Returns:
    - OrganizationResponse: The updated organization details

    Raises:
    - 404: Organization not found
    """
    try:
        data = OrganizationUpdateRequestDTO.model_validate(request)
        result = service.update_organization(
            organization_id,
            data,
        )
        return OrganizationResponse.model_validate(result)
    except OrganizationNotFound as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exception)
        ) from exception


@router.delete("/{organization_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_organization(
    organization_id: UUID,
    _: AdminContext = Depends(get_current_admin),
    service: OrganizationService = Depends(get_organization_service),
):
    """
    Delete an organization.

    Parameters:
        organization_id: UUID of the organization to delete

    Returns:
        No content (204) on successful deletion

    Raises:
        404: Organization not found
        409: If the organization is in use and cannot be deleted.
    """
    try:
        service.delete_organization(
            organization_id,
        )
    except OrganizationNotFound as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exception)
        ) from exception

    except OrganizationInUse as exception:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exception)
        ) from exception


@router.post("/{organization_id}/activate", status_code=status.HTTP_204_NO_CONTENT)
def activate_organization(
    organization_id: UUID,
    _: AdminContext = Depends(get_current_admin),
    service: OrganizationService = Depends(get_organization_service),
):
    """
    Activate an organization.

    Parameters:
        organization_id: UUID of the organization to activate

    Returns:
        No content (204) on successful deletion

    Raises:
        404: Organization not found
    """
    try:
        service.activate(
            organization_id=organization_id
        )
    except OrganizationNotFound as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exception)
        ) from exception


@router.post("/{organization_id}/deactivate", status_code=status.HTTP_204_NO_CONTENT)
def deactivate_organization(
    organization_id: UUID,
    _: AdminContext = Depends(get_current_admin),
    service: OrganizationService = Depends(get_organization_service),
):
    """
    Deactivate an organization.

    Parameters:
        organization_id: UUID of the organization to deactivate

    Returns:
        No content (204) on successful deletion

    Raises:
        404: Organization not found
    """
    try:
        service.deactivate(
            organization_id=organization_id
        )
    except OrganizationNotFound as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exception)
        ) from exception
