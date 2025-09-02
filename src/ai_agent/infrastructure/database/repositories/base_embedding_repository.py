"""
Repository interface for managing Embedding entities.

This module defines the abstract interface for Embedding persistence operations
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from uuid import UUID

from ai_agent.domain.dtos.embedding_dto import EmbeddingCreateDTO
from ai_agent.domain.dtos.search_dto import SearchDTO
from ai_agent.domain.models.database_entities.embedding import Embedding


class BaseEmbeddingRepository(ABC):
    """
    Abstract base class for embedding repository operations.

    Defines methods for storing and retrieving vector embeddings.
    """

    @abstractmethod
    def create(
        self,
        data: EmbeddingCreateDTO,
        organization_id: UUID
    ) -> Embedding:
        """
        Create a new embedding.

        Args:
            data (EmbeddingCreateDTO): The embedding data to store.
            organization_id (UUID): ID of the organization

        Returns:
            Embedding: The created embedding entity.
        """

    @abstractmethod
    def get_list(
        self,
        organization_id: UUID,
        document_id: Optional[UUID] = None,
        category_id: Optional[UUID] = None,
        collection_id: Optional[UUID] = None,
    ) -> List[Embedding]:
        """
        Retrieve all embeddings filtered by document/category/collection if provided.

        Args:
            organization_id (UUID): ID of the organization
            document_id (Optional[UUID]): Filter by document.
            category_id (Optional[UUID]): Filter by category of document.
            collection_id (Optional[UUID]): Filter by collection of category.

        Returns:
            List[Embedding]: Matching embeddings.
        """

    @abstractmethod
    def delete(
        self,
        organization_id: UUID,
        document_id: Optional[UUID] = None,
        category_id: Optional[UUID] = None,
        collection_id: Optional[UUID] = None,
    ) -> None:
        """
        Delete embeddings filtered by document/category/collection.

        Args:
            organization_id (UUID): ID of the organization
            document_id (Optional[UUID]): Filter by document.
            category_id (Optional[UUID]): Filter by category.
            collection_id (Optional[UUID]): Filter by collection.
        """

    # pylint: disable=too-many-arguments, too-many-positional-arguments
    @abstractmethod
    def search(
        self,
        organization_id: UUID,
        data: SearchDTO,
    ) -> List[Tuple[Embedding, float]]:
        """
        Search for similar embeddings based on vector similarity.

        This abstract method defines the interface for performing semantic searches
        against stored embeddings. The search uses vector similarity to find the most
        relevant content based on the provided query vector.

        Args:
            organization_id (UUID): ID of the organization
            data (SearchDTO): containing data for searching:
                query_vector (List[float]): The vector representation of the query to compare
                                        against stored embeddings.
                top_k (int): The maximum number of results to return, ordered by similarity.
                document_id (Optional[UUID]): If provided, limits the search to embeddings
                                            associated with a specific document.
                category_id (Optional[UUID]): If provided, limits the search to embeddings
                                            within a specific category.
                collection_ids (Optional[List[UUID]]): If provided, limits the search to embeddings
                                            within specific collections.

        Returns:
            List[Tuple[Embedding, float]]: A list of tuples, each containing:
                - An Embedding object representing a match
                - A float indicating the distance score (lower is more similar)
            The list is ordered by similarity (most similar first).

        Note:
            At least one of document_id, category_id, or collection_id should be provided
            to properly scope the search. Implementations may choose to enforce this requirement.

        Raises:
            NotImplementedError: This is an abstract method that must be implemented by subclasses.
        """
