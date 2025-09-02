"""
Dependency injection module for organization-related services.
"""

from fastapi import Depends

from ai_agent.api.dependencies.password_hasher_dependencies import \
    get_password_hasher
from ai_agent.api.dependencies.repository_dependencies import (
    get_collection_repository, get_organization_repository)
from ai_agent.application.services.database_services import OrganizationService
from ai_agent.infrastructure.database.repositories import \
    BaseOrganizationRepository, BaseCollectionRepository
from ai_agent.infrastructure.password_hasher.base_password_hasher import \
    BasePasswordHasher


def get_organization_service(
    organization_repository: BaseOrganizationRepository = Depends(
        get_organization_repository
    ),
    collection_repository: BaseCollectionRepository = Depends(
        get_collection_repository
    ),
    password_hasher: BasePasswordHasher = Depends(
        get_password_hasher
    )
) -> OrganizationService:
    """
    Factory function that provides a configured OrganizationService instance.

    Args:
        organization_repository (BaseOrganizationRepository): The organization repository,
            injected via dependency.
        collection_repository (BaseCollectionRepository):
            The collection repository working with collection table
        password_hasher (BasePasswordHasher):
                Password hashing service for securing passwords

    Returns:
        OrganizationService: A configured organization service.
    """
    return OrganizationService(
        organization_repository=organization_repository,
        collection_repository=collection_repository,
        password_hasher=password_hasher
    )
