"""
Document API endpoints.

This module contains endpoints for handling document file
"""

from typing import List, Optional
from uuid import UUID

from fastapi import (APIRouter, Depends, File, Form, HTTPException, Path,
                     Query, UploadFile, status)

from ai_agent.api.dependencies.security_dependencies import \
    get_current_organization
from ai_agent.api.dependencies.service_dependencies.document_service_dependencies import \
    get_document_service
from ai_agent.api.helpers.file_helper import save_temp_file
from ai_agent.api.schemas.documents import DocumentResponse, DocumentUpdate
from ai_agent.api.schemas.download import DownloadResponse
from ai_agent.application.services.database_services import DocumentService
from ai_agent.domain.dtos.document_dto import (DocumentCreateRequestDTO,
                                               DocumentUpdateDTO)
from ai_agent.domain.exceptions.auth_exceptions import InsufficientScope
from ai_agent.domain.exceptions.category_exceptions import CategoryNotFound
from ai_agent.domain.exceptions.collection_exceptions import CollectionNotFound
from ai_agent.domain.exceptions.document_exceptions import (DocumentDeleted,
                                                            DocumentNotFound)
from ai_agent.domain.models.security_contexts.organization_context import \
    OrganizationContext

router = APIRouter()


@router.post("/documents/upload", response_model=DocumentResponse)
async def upload_document(
        file: UploadFile = File(..., description="List of files to upload"),
        name: Optional[str] = Form(None, description="Name of the document"),
        category_id: UUID = Form(..., description="Id of the category the file belongs to"),
        service: DocumentService = Depends(get_document_service),
        organization_context: OrganizationContext = Depends(get_current_organization),
):
    """
    Upload a document file and create a document record in the system.

    The file is saved to to the storage system and its
    storage URI is registered along with other document information,
    save to the documents table

    Args:
        file (UploadFile): The document file to be uploaded
        name (str): A custom name for identifying the document
        category_id (UUID): The category this document belongs to

    Returns:
        DocumentResponse:  The newly created document response.

    Raises:
        404: If the specified category is not found
        403: If the client does not have the required scope.
    """
    try:
        local_uri = await save_temp_file(file)
        assert file.filename is not None
        data = DocumentCreateRequestDTO(
            custom_name=name or file.filename,
            filename=file.filename,
            storage_uri=local_uri,
            category_id=category_id
        )
        result = service.create_document(
            data,
            organization_context=organization_context
        )
        return DocumentResponse.model_validate(result)


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


@router.get("/collections/{collection_id}/documents", response_model=List[DocumentResponse])
async def get_list_documents(
    collection_id: UUID = Path(description="Collection ID the documents belong to"),
    category_id: Optional[UUID] = Query(None, description="Filter by category ID"),
    service: DocumentService = Depends(get_document_service),
    organization_context: OrganizationContext = Depends(get_current_organization),
):
    """
    Get a list of documents, optionally filtered by collection or category.

    Args:
        collection_id (UUID): Collection ID the documents belong to
        category_id (UUID, optional): Filter by category ID

    Returns:
        List[DocumentResponse]: Filtered list of documents

    Raises:
        404: If provided collection/category ID does not exist
        403: If the client does not have the required scope.
    """
    try:
        results = service.get_list_documents(
            organization_context=organization_context,
            collection_id=collection_id,
            category_id=category_id
        )
        return [DocumentResponse.model_validate(document) for document in results]


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

    except CollectionNotFound as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exception)
        ) from exception


@router.get("/documents/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: UUID = Path(..., description="ID of the document to retrieve"),
    service: DocumentService = Depends(get_document_service),
    organization_context: OrganizationContext = Depends(get_current_organization),
):
    """
    Retrieve a single document by its ID.

    Args:
        document_id (UUID): The ID of the document to retrieve.

    Returns:
        DocumentResponse: The document details.

    Raises:
        404: If the document is not found.
        403: If the client does not have the required scope.
    """
    try:
        result = service.get_document(
            document_id,
            organization_context=organization_context
        )
        return DocumentResponse.model_validate(result)


    except InsufficientScope as exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exception)
        ) from exception

    except DocumentNotFound as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exception)
        ) from exception


@router.get("/documents/{document_id}/download", response_model=DownloadResponse)
async def download_document(
    document_id: UUID = Path(..., description="ID of document to download"),
    service: DocumentService = Depends(get_document_service),
    organization_context: OrganizationContext = Depends(get_current_organization),
):
    """
    Down load a document with a given ID

    Args:
        document_id (UUID): ID of document to download

    Returns:
        FileResponse: The downloaded document file.

    Raises:
        404: If the document does not exist.
        403: If the client does not have the required scope.
    """
    try:
        result = service.download_document(
            document_id,
            organization_context=organization_context
        )
        return DownloadResponse.model_validate({**result.model_dump(), "id": document_id})


    except InsufficientScope as exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exception)
        ) from exception

    except DocumentNotFound as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exception)
        ) from exception


@router.delete("/documents/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    document_id: UUID,
    service: DocumentService = Depends(get_document_service),
    organization_context: OrganizationContext = Depends(get_current_organization),
):
    """
    Delete a document by its ID.
    Using soft deletion, the document status is marked as DELETED

    Args:
        document_id (UUID): The unique identifier of the document to delete.

    Returns:
        None: Returns no content on successful deletion.

    Raises:
        404: If the document with the specified ID doesn't exist.
        409: If the document with the specified ID already in deleted state.
        403: If the client does not have the required scope.

    Example:
        DELETE /documents/123e4567-e89b-12d3-a456-426614174000
    """
    try:
        service.soft_delete_document(
            document_id,
            organization_context=organization_context
        )


    except InsufficientScope as exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exception)
        ) from exception

    except DocumentNotFound as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exception)
        ) from exception

    except DocumentDeleted as exception:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exception)
        ) from exception


@router.patch("/documents/{document_id}", response_model=DocumentResponse)
def update_document(
    document_id: UUID,
    request: DocumentUpdate,
    service: DocumentService = Depends(get_document_service),
    organization_context: OrganizationContext = Depends(get_current_organization),
):
    """
    Update a document by ID.

    Args:
        document_id (UUID): The ID of the document to update.
        request (DocumentUpdate): Fields to update.

    Returns:
        DocumentResponse: The updated document.

    Raises:
        404: If the document does not exist or
            the category does not exists in the current collection.
        403: If the client does not have the required scope.
    """
    try:
        document_dto = DocumentUpdateDTO.model_validate(request)
        updated_document = service.update_document(
            document_id,
            document_dto,
            organization_context=organization_context
        )
        return DocumentResponse.model_validate(updated_document)


    except InsufficientScope as exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exception)
        ) from exception

    except (DocumentNotFound, CategoryNotFound) as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exception)
        ) from exception
