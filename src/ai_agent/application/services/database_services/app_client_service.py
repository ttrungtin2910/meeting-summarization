"""
AppClient Service Module.
"""

import secrets
from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID, uuid4

from ai_agent.domain.dtos.app_client_dto import (AppClientCreateDTO,
                                                 AppClientCreateRequestDTO,
                                                 AppClientUpdateDTO)
from ai_agent.domain.exceptions.app_client_exceptions import (
    AppClientAlreadyExists, AppClientNotFound)
from ai_agent.domain.exceptions.collection_exceptions import CollectionNotFound
from ai_agent.domain.models.database_entities.app_client import AppClient
from ai_agent.domain.models.database_entities.collection import Collection
from ai_agent.domain.models.security_contexts.organization_context import \
    OrganizationContext
from ai_agent.infrastructure.database.repositories import (
    BaseAppClientRepository, BaseCollectionRepository,
    BaseOrganizationRepository)


class AppClientService:
    """
    Service class for managing AppClient operations.

    This service encapsulates business logic for app client management,
    utilizing the repository pattern for data access.
    """

    def __init__(
        self,
        app_client_repository: BaseAppClientRepository,
        organization_repository: BaseOrganizationRepository,
        collection_repository: BaseCollectionRepository
    ):
        """
        Initialize the AppClientService.

        Args:
            app_client_repository (BaseAppClientRepository): repository for AppClient.
            organization_repository (BaseOrganizationRepository):
                repository for Organization validation.
            collection_repository (BaseCollectionRepository):
                repository for collection validation.
        """
        self.app_client_repository = app_client_repository
        self.organization_repository = organization_repository
        self.collection_repository = collection_repository

    def create_app_client(
        self,
        data: AppClientCreateRequestDTO,
        organization_context: OrganizationContext
    ) -> AppClient:
        """
        Create a new AppClient for a given organization.

        Args:
            data (AppClientCreateDTO): The client creation input.
            organization_context (OrganizationContext): The authenticated organization context

        Returns:
            AppClient: The created app client.

        Raises:
            OrganizationNotFound: If the organization does not exist.
            AppClientAlreadyExists: If client_id is already used.
        """
        organization_id = organization_context.organization_id

        # Check if app client name exists in the organization
        if self.app_client_repository.exists(
            name=data.name,
            organization_id=organization_id
        ):
            raise AppClientAlreadyExists(data.name)

        # Check if collection_id exists in the organization
        existed_collections: List[Collection] = self.collection_repository.get_list(
            organization_id=organization_id
        )

        existed_collection_ids = [collection.id for collection in existed_collections]
        for collection_id in data.collection_ids:
            if collection_id not in existed_collection_ids:
                raise CollectionNotFound(collection_id=collection_id)

        # Create dto
        app_client_create_dto = AppClientCreateDTO(
            **data.model_dump(),
            client_id=uuid4(),
            client_secret=secrets.token_urlsafe(40),
            is_active=True,
            created_at=datetime.now(timezone.utc)
        )

        return self.app_client_repository.create(
            app_client_create_dto,
            organization_id=organization_id
        )

    def update_app_client(
        self,
        client_id: UUID,
        organization_context: OrganizationContext,
        data: AppClientUpdateDTO,
    ) -> AppClient:
        """
        Update an existing AppClient.

        Args:
            client_id (UUID): The ID of the client to update.
            organization_context (OrganizationContext): The authenticated organization context
            data (AppClientUpdateDTO): Fields to update.

        Returns:
            AppClient: The updated AppClient.

        Raises:
            OrganizationNotFound: If org is invalid.
            AppClientNotFound: If client doesn't exist.
        """
        organization_id = organization_context.organization_id

        # check if app client with the specific ID exists
        existing_app_client: Optional[AppClient] = self.app_client_repository.get_by_client_id(
            client_id=client_id,
        )
        if not existing_app_client or existing_app_client.organization_id != organization_id:
            raise AppClientNotFound(client_id=client_id)

        # Check if collection_id exists in the organization
        if data.collection_ids:
            existed_collections: List[Collection] = self.collection_repository.get_list(
                organization_id=organization_id
            )
            existed_collection_ids = [collection.id for collection in existed_collections]
            for collection_id in data.collection_ids:
                if collection_id not in existed_collection_ids:
                    raise CollectionNotFound(collection_id=collection_id)


        # Check if no field changed compared to the existed app client
        has_changed = False
        update_data = data.model_dump(exclude_unset=True, exclude_none=True)
        for field, new_value in update_data.items():
            old_value = getattr(existing_app_client, field, None)
            if new_value != old_value:
                has_changed = True
                break

        # If no change, return the existing_app_client
        if not has_changed:
            return existing_app_client

        # Check if updated name exists in the organization
        if data.name:
            app_client_same_name = self.app_client_repository.get_by_name(
                name=data.name,
                organization_id=organization_id
            )
            if app_client_same_name and app_client_same_name.client_id != client_id:
                raise AppClientAlreadyExists(data.name)

        # Check if updated collection_id exists in the organization
        if data.collection_ids:
            existed_collections: List[Collection] = self.collection_repository.get_list(
                organization_id=organization_id
            )

            existed_collection_ids = [collection.id for collection in existed_collections]
            for collection_id in data.collection_ids:
                if collection_id not in existed_collection_ids:
                    raise CollectionNotFound(collection_id=collection_id)

        updated_app_client = self.app_client_repository.update(
            client_id=client_id,
            organization_id=organization_id,
            data=data
        )
        assert updated_app_client is not None
        return updated_app_client

    def get_by_id(self, client_id: UUID, organization_context: OrganizationContext) -> AppClient:
        """
        Retrieve an AppClient by its client_id within a specific organization.

        Parameters:
            client_id (UUID): The unique identifier of the AppClient to retrieve.
            organization_context (OrganizationContext): The authenticated organization context

        Returns:
            AppClient: The AppClient object if found.

        Raises:
            AppClientNotFound: If the AppClient with the specified client_id
                is not found within the organization.
        """
        organization_id = organization_context.organization_id

        # check if app client with the specific ID exists
        existing_app_client: Optional[AppClient] = self.app_client_repository.get_by_client_id(
            client_id=client_id,
        )
        if not existing_app_client or existing_app_client.organization_id != organization_id:
            raise AppClientNotFound(client_id=client_id)
        return existing_app_client

    def get_by_name(self, name: str, organization_context: OrganizationContext) -> AppClient:
        """
        Retrieve an AppClient by its name within a specific organization.

        Parameters:
            name (str): The name of the AppClient to retrieve.
            organization_context (OrganizationContext): The authenticated organization context

        Returns:
            AppClient: The AppClient object if found.

        Raises:
            AppClientNotFound: If the AppClient with the specified name
                is not found within the organization.
        """
        organization_id = organization_context.organization_id

        client = self.app_client_repository.get_by_name(name, organization_id)
        if not client:
            raise AppClientNotFound(client_name=name)
        return client

    def list_app_clients(self, organization_context: OrganizationContext) -> List[AppClient]:
        """
        List all AppClients associated with a specific organization.

        Parameters:
            organization_context (OrganizationContext): The authenticated organization context

        Returns:
            List[AppClient]: A list of AppClient objects associated with the organization.
        """
        organization_id = organization_context.organization_id

        return self.app_client_repository.list_by_organization(organization_id)

    def delete_app_client(self, client_id: UUID, organization_context: OrganizationContext) -> None:
        """
        Delete an AppClient by its client_id within a specific organization.

        Parameters:
            client_id (UUID): The unique identifier of the AppClient to delete.
            organization_context (OrganizationContext): The authenticated organization context

        Raises:
            OrganizationNotFound: If the organization with the specified organization_id
                does not exist.
            AppClientNotFound: If the AppClient with the specified client_id
                is not found within the organization.
        """
        organization_id = organization_context.organization_id

        # check if app client with the specific ID exists
        existing_app_client: Optional[AppClient] = self.app_client_repository.get_by_client_id(
            client_id=client_id,
        )
        if not existing_app_client or existing_app_client.organization_id != organization_id:
            raise AppClientNotFound(client_id=client_id)

        self.app_client_repository.delete(client_id, organization_id)
