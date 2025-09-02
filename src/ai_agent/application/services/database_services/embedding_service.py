"""
Embedding Service Module
"""

from datetime import datetime, timezone
from typing import List, Optional, Tuple
from uuid import UUID

from ai_agent.domain.dtos.embedding_dto import (EmbeddingCreateDTO,
                                                EmbeddingCreateRequestDTO)
from ai_agent.domain.dtos.search_dto import SearchDTO, SearchRequestDTO
from ai_agent.domain.exceptions.category_exceptions import CategoryNotFound
from ai_agent.domain.exceptions.collection_exceptions import CollectionNotFound
from ai_agent.domain.exceptions.document_exceptions import DocumentNotFound
from ai_agent.domain.exceptions.organization_exceptions import \
    OrganizationNotFound
from ai_agent.domain.models.database_entities.embedding import Embedding
from ai_agent.infrastructure.database.repositories import (
    BaseCategoryRepository, BaseCollectionRepository, BaseDocumentRepository,
    BaseEmbeddingRepository, BaseOrganizationRepository)


class EmbeddingService:
    """
    Service class for managing Embedding operations.
    """

    def __init__(
        self,
        collection_repository: BaseCollectionRepository,
        category_repository: BaseCategoryRepository,
        document_repository: BaseDocumentRepository,
        embedding_repository: BaseEmbeddingRepository,
        organization_repository: BaseOrganizationRepository
    ):
        """
        Initialize the EmbeddingService with a Embedding repository

        Args:
            collection_repository (BaseCollectionRepository): Repository for collection data access.
            document_repository (BaseDocumentRepository): Interface to access documents.
            category_repository (BaseCategoryRepository): Interface to access categories.
            embedding_repository (BaseEmbeddingRepository): Interface to access embeddings.
            organization_repository (BaseOrganizationRepository): repository for organization table
        """
        self.collection_repository = collection_repository
        self.document_repository = document_repository
        self.category_repository = category_repository
        self.embedding_repository = embedding_repository
        self.organization_repository = organization_repository

    def create_embedding(
            self,
            data: EmbeddingCreateRequestDTO,
            organization_id: UUID
        ) -> Embedding:
        """
        Create a new embedding.

        Args:
            data (EmbeddingCreateRequestDTO): Data to create the document.
            organization_id (UUID): ID of the organization

        Returns:
            Embedding: The created document.

        Raises:
            DocumentNotFound: If the document with the given ID does not exist
        """
        # Check if organization exists
        if not self.organization_repository.exists(organization_id=organization_id):
            raise OrganizationNotFound

        # Check if the document exists
        document_id: UUID = data.document_id
        document = self.document_repository.get(
            document_id,
            organization_id=organization_id
        )

        if not document:
            raise DocumentNotFound(document_id=document_id)

        # Create DTO object
        embedding_dto = EmbeddingCreateDTO(
            **data.model_dump(),
            created_at=datetime.now(tz=timezone.utc),
        )

        # Save to table
        return self.embedding_repository.create(
            embedding_dto,
            organization_id=organization_id
        )

    def delete_embedding(
            self,
            organization_id: UUID,
            document_id: Optional[UUID] = None,
            category_id: Optional[UUID] = None,
            collection_id: Optional[UUID] = None
        ) -> None:
        """
        Delete embeddings based on optional filters: document, category, or collection.

        Args:
            organization_id (UUID): ID of the organization
            document_id (Optional[UUID]): Filter by document ID.
            category_id (Optional[UUID]): Filter by category ID.
            collection_id (Optional[UUID]): Filter by collection ID.

        Raises:
            ValueError: If no filter is provided.
            DocumentNotFound: If document_id is provided but not found.
            CategoryNotFound: If category_id is provided but not found.
            CollectionNotFound: If collection_id is provided but not found.
        """
        # Check if organization exists
        if not self.organization_repository.exists(organization_id=organization_id):
            raise OrganizationNotFound

        # Require at least one filter to avoid full delete
        if not document_id and not category_id and not collection_id:
            raise ValueError("At least one filter must be provided to delete embeddings.")

        # Validate document if provided
        if document_id:
            document = self.document_repository.get(
                document_id,
                organization_id=organization_id
            )
            if not document:
                raise DocumentNotFound(document_id=document_id)

        # Validate category if provided
        if category_id:
            category = self.category_repository.get_by_id(
                category_id,
                organization_id=organization_id
            )
            if not category:
                raise CategoryNotFound(category_id=category_id)

        # Validate collection if provided
        if collection_id:
            collection = self.collection_repository.get_by_id(
                collection_id,
                organization_id=organization_id
            )
            if not collection:
                raise CollectionNotFound(collection_id=collection_id)

        # Perform deletion
        self.embedding_repository.delete(
            organization_id=organization_id,
            document_id=document_id,
            category_id=category_id,
            collection_id=collection_id,
        )

    def search_embedding(
            self,
            organization_id: UUID,
            search_request: SearchRequestDTO
        ) -> List[Tuple[Embedding, float]]:
        """
        Search for the top-k most similar embeddings based on the input query vector.

        Supports optional scoping by document, category, or collection.

        Args:
            organization_id (UUID): ID of the organization
            search_request (SearchRequestDTO): DTO containing search parameters.

        Returns:
            List[Tuple[Embedding, float]]:
            List of Embedding domain objects with similarity_score set.

        Raises:
            ValueError: If query_vector is empty or top_k is invalid.
            DocumentNotFound: If document_id is provided but not found.
            CategoryNotFound: If category_id is provided but not found.
            CollectionNotFound: If collection_id is provided but not found.
        """
        # Check if organization exists
        if not self.organization_repository.exists(organization_id=organization_id):
            raise OrganizationNotFound

        # Extract search data
        query_vector: List[float] = search_request.query_vector
        top_k: int = search_request.top_k
        document_id: Optional[UUID] = search_request.document_id
        category_id: Optional[UUID] = search_request.category_id
        collection_id: Optional[UUID] = search_request.collection_id

        # Validate
        if not query_vector:
            raise ValueError("Query vector must not be empty.")

        if top_k <= 0:
            raise ValueError("top_k must be greater than zero.")

        # Optional validations
        if document_id:
            document = self.document_repository.get(
                document_id,
                organization_id=organization_id
            )
            if not document:
                raise DocumentNotFound(document_id=document_id)

        if category_id:
            category = self.category_repository.get_by_id(
                category_id,
                organization_id=organization_id
            )
            if not category:
                raise CategoryNotFound(category_id=category_id)

        if collection_id:
            collection = self.collection_repository.get_by_id(
                collection_id,
                organization_id=organization_id
            )
            if not collection:
                raise CollectionNotFound(collection_id=collection_id)

        # Create dto
        search_dto: SearchDTO = SearchDTO.model_validate(search_request)

        # Perform vector similarity search
        return self.embedding_repository.search(
            organization_id=organization_id,
            data=search_dto
        )
