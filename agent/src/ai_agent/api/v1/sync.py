"""
Sync API endpoints.

This module contains endpoints for sync documents into Embedding table
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from ai_agent.api.dependencies.security_dependencies import \
    get_current_organization
from ai_agent.api.dependencies.service_dependencies.sync_service_dependencies import \
    get_document_sync_service
from ai_agent.api.schemas.sync import SyncResponse
from ai_agent.application.services.sync_services.document_sync_service import \
    DocumentSyncService
from ai_agent.domain.dtos.sync_dto import SyncResponseDTO
from ai_agent.domain.exceptions.auth_exceptions import InsufficientScope
from ai_agent.domain.exceptions.collection_exceptions import CollectionNotFound
from ai_agent.domain.models.security_contexts.client_context import \
    ClientContext
from ai_agent.domain.models.security_contexts.organization_context import \
    OrganizationContext

router = APIRouter(prefix="/sync")


@router.post(
        "/collections/{collection_id}",
        response_model=SyncResponse)
def sync_collection_documents(
    collection_id: UUID,
    sync_service: DocumentSyncService = Depends(get_document_sync_service),
    organization_context: OrganizationContext = Depends(get_current_organization),
):
    """
    Synchronize documents in a specific collection.

    Args:
        collection_id (UUID): The unique identifier of the collection to synchronize

    Returns:
        SyncResponse: Statistics about the synchronization operation, including:
            - id: The collection ID that was synchronized
            - added: Number of new documents processed
            - deleted: Number of documents removed
            - updated: Number of documents updated

    Raises:
        404: If provided collection ID does not exist
        403: If the client does not have the required scope.
    """
    try:
        result: SyncResponseDTO = sync_service.sync_documents(
            collection_id,
            organization_context=organization_context
        )

        return SyncResponse(
            collection_id=collection_id,
            **result.model_dump()
        )

    except InsufficientScope as exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exception)
        ) from exception

    except CollectionNotFound as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exception)
        ) from exception
