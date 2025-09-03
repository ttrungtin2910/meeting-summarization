"""
Collection API Router Module
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from ai_agent.api.dependencies.security_dependencies import \
    get_current_organization
from ai_agent.api.dependencies.service_dependencies.collection_service_dependencies import \
    get_collection_service
from ai_agent.api.schemas.collections import (CollectionCreate,
                                              CollectionResponse,
                                              CollectionUpdate)
from ai_agent.application.services.database_services import CollectionService
from ai_agent.domain.dtos.collection_dto import (CollectionCreateRequestDTO,
                                                 CollectionUpdateDTO)
from ai_agent.domain.exceptions.auth_exceptions import InsufficientScope
from ai_agent.domain.exceptions.collection_exceptions import (
    CollectionAlreadyExists, CollectionInUseError, CollectionNotFound)
from ai_agent.domain.models.security_contexts.organization_context import \
    OrganizationContext

router = APIRouter(prefix="/collections")


@router.post("", response_model=CollectionResponse)
def create_collection(
    request: CollectionCreate,
    organization_context: OrganizationContext = Depends(get_current_organization),
    service: CollectionService = Depends(get_collection_service),
):
    """
    Endpoint to create a new collection for the current client.
    Args:
        request (CollectionCreate): The request object containing the details
            of the collection to be created.

    Returns:
        CollectionResponse: The response model containing the details of the
        newly created collection.

    Raises:
        HTTPException:
            409: If a collection with the same name already exists.
    """
    try:
        data = CollectionCreateRequestDTO(
            name=request.name
        )
        result = service.create_collection(
            organization_context=organization_context,
            data=data,
        )
        return CollectionResponse.model_validate(result)

    except CollectionAlreadyExists as exception:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exception)
        ) from exception


@router.get("/{collection_id}", response_model=CollectionResponse)
def get_collection(
    collection_id: UUID,
    organization_context: OrganizationContext = Depends(get_current_organization),
    service: CollectionService = Depends(get_collection_service),
):
    """
    Retrieve a collection by its unique identifier.

    Args:
        collection_id (UUID): The unique identifier of the collection to retrieve.

    Returns:
        CollectionResponse: The collection metadata, including name, description, and timestamps.

    Raises:
        404: If no collection with the specified ID is found.

    Example:
        GET /collections/5f3a6e3b-8df2-4b8e-932c-709d2de3795f
    """
    try:
        result = service.get_collection(
            collection_id,
            organization_context=organization_context,
        )
        return CollectionResponse.model_validate(result)

    except CollectionNotFound as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exception)
        ) from exception

@router.get("", response_model=list[CollectionResponse])
def get_list_collection(
    organization_context: OrganizationContext = Depends(get_current_organization),
    service: CollectionService = Depends(get_collection_service),
):
    """
    Retrieve a list of all collections.

    Returns:
        list[CollectionResponse]: A list of all collections.

    Raises:
        400: If there is an error retrieving the list of collections.
    """
    try:
        collections = service.get_list_collections(organization_context=organization_context)
        return [CollectionResponse.model_validate(collection) for collection in collections]
    except Exception as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exception)
        ) from exception

@router.patch("/{collection_id}", response_model=CollectionResponse)
def update_collection(
    collection_id: UUID,
    collection: CollectionUpdate,
    organization_context: OrganizationContext = Depends(get_current_organization),
    service: CollectionService = Depends(get_collection_service),
    ):
    """
    Update the name of an existing collection.

    Args:
        collection_id (UUID): The unique identifier of the collection to update.
        collection (CollectionUpdate): The new values for the collection.

    Returns:
        CollectionResponse: The updated collection data.

    Raises:
        400: If the collection does not exist or the update fails.

    Example:
        PATCH /collections/5f3a6e3b-8df2-4b8e-932c-709d2de3795f
        Body: { "name": "Updated Collection Name" }
    """

    try:
        collection_dto = CollectionUpdateDTO(**collection.model_dump(exclude_unset=True))
        result = service.update_collection(
            collection_id,
            collection_dto,
            organization_context=organization_context,
        )
        return CollectionResponse.model_validate(result)
    except CollectionNotFound as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exception)
        ) from exception


@router.delete("/{collection_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_collection(
    collection_id: UUID,
    organization_context: OrganizationContext = Depends(get_current_organization),
    service: CollectionService = Depends(get_collection_service),
):
    """
    Delete a collection by its ID.

    Args:
        collection_id (UUID): The unique identifier of the collection to delete.

    Returns:
        None: Returns no content on successful deletion.

    Raises:
        404: If the collection with the specified ID doesn't exist.
        409: If the collection is in use and cannot be deleted.

    Example:
        DELETE /collections/123e4567-e89b-12d3-a456-426614174000
    """
    try:
        service.delete_collection(
            collection_id,
            organization_context=organization_context,
        )

    except CollectionNotFound as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exception)
        ) from exception

    except CollectionInUseError as exception:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exception)
        ) from exception
