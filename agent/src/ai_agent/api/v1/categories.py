"""
Category API endpoints.

This module defines the FastAPI routes for category management,
providing endpoints for creating, retrieving, listing, and deleting categories.
"""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from ai_agent.api.dependencies.security_dependencies import \
    get_current_organization
from ai_agent.api.dependencies.service_dependencies.category_service_dependencies import \
    get_category_service
from ai_agent.api.schemas.categories import (CategoryCreate,
                                             CategoryMinimalResponse,
                                             CategoryResponse, CategoryUpdate)
from ai_agent.application.services.database_services import CategoryService
from ai_agent.domain.dtos.category_dto import (CategoryCreateRequestDTO,
                                               CategoryUpdateDTO)
from ai_agent.domain.exceptions.auth_exceptions import InsufficientScope
from ai_agent.domain.exceptions.category_exceptions import (
    CategoryAlreadyExists, CategoryInUseError, CategoryNotFound)
from ai_agent.domain.exceptions.collection_exceptions import CollectionNotFound
from ai_agent.domain.models.security_contexts.organization_context import \
    OrganizationContext

# Define router
router = APIRouter()


@router.post("/collections/{collection_id}/categories", response_model=CategoryResponse)
def create_category(
    collection_id: UUID,
    request: CategoryCreate,
    service: CategoryService = Depends(get_category_service),
    organization_context: OrganizationContext = Depends(get_current_organization)
):
    """
    Create a new category

    This endpoint allows clients to create a new category with the given name in a collection

    Args:
        collection_id (UUID): Id of the collection that the category belongs to
        request (CategoryCreate): The request body containing:
            - name (str)
            - collection_id (UUID)

    Returns:
        CategoryResponse: The created category data.

    Raises:
        404: If the collection with the collection_id does not exist.
        409: If a category with the same name already exists.
        403: If the client does not have the required scope
    """
    try:
        data = CategoryCreateRequestDTO(
            name=request.name,
            collection_id=collection_id
        )
        result = service.create_category(
            data,
            organization_context=organization_context)
        return CategoryResponse.model_validate(result)
    except InsufficientScope as exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exception)
        ) from exception
    # If the collection with the collection_id does not exist.
    except CollectionNotFound as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exception),
        ) from exception

    # If a category with the same name already exists.
    except CategoryAlreadyExists as exception:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exception)
        ) from exception


@router.get("/categories/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: UUID,
    service: CategoryService = Depends(get_category_service),
    organization_context: OrganizationContext = Depends(get_current_organization)
):
    """
    Get a single category by ID.

    Args:
        category_id (UUID): The ID of the category to retrieve.

    Returns:
        CategoryResponse: The retrieved category.

    Raises:
        403: If the client does not have the required scope
        404: If the category does not exist.
    """
    try:
        category = service.get_category(
            category_id,
            organization_context=organization_context
        )
        return CategoryResponse.model_validate(category)

    except InsufficientScope as exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exception)
        ) from exception

    except CategoryNotFound as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exception),
        ) from exception


@router.get(
        "/collections/{collection_id}/categories",
        response_model=List[CategoryMinimalResponse]
    )
def get_list_categories(
    collection_id: UUID,
    service: CategoryService = Depends(get_category_service),
    organization_context: OrganizationContext = Depends(get_current_organization)
):
    """
    Get all categories in a given collection.

    Args:
        collection_id (UUID): The ID of the collection.

    Returns:
        List[CategoryResponse]: List of categories in the collection.

    Raises:
        403: If the client does not have the required scope
        404: If the collection does not exist.
    """
    try:
        categories = service.get_list_categories(
            collection_id,
            organization_context=organization_context
        )
        return [CategoryMinimalResponse.model_validate(category) for category in categories]

    except InsufficientScope as exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exception)
        ) from exception

    except CollectionNotFound as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exception),
        ) from exception


@router.patch("/categories/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: UUID,
    request: CategoryUpdate,
    service: CategoryService = Depends(get_category_service),
    organization_context: OrganizationContext = Depends(get_current_organization)
):
    """
    Update a category by ID.

    Args:
        category_id (UUID): The ID of the category to update.
        request (CategoryUpdate): Fields to update.

    Returns:
        CategoryResponse: The updated category.

    Raises:
        403: If the client does not have the required scope
        404: If the category does not exist.
        409: If a category with the same name already exists.
    """
    try:
        dto = CategoryUpdateDTO.model_validate(request)
        updated = service.update_category(
            category_id,
            dto,
            organization_context=organization_context
        )
        return CategoryResponse.model_validate(updated)

    except InsufficientScope as exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exception)
        ) from exception

    except CategoryNotFound as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exception)
        ) from exception

    except CategoryAlreadyExists as exception:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exception)
        ) from exception


@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: UUID,
    service: CategoryService = Depends(get_category_service),
    organization_context: OrganizationContext = Depends(get_current_organization)
):
    """
    Delete a category by ID.

    Args:
        category_id (UUID): The ID of the category to delete.

    Raises:
        403: If the client does not have the required scope
        404: If the category does not exist.
        409: If the category is in use and cannot be deleted.
    """
    try:
        service.delete_category(
            category_id,
            organization_context=organization_context
        )

    except InsufficientScope as exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exception)
        ) from exception

    except CategoryNotFound as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exception)
        ) from exception

    except CategoryInUseError as exception:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exception)
        ) from exception
