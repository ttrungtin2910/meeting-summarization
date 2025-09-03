"""
Repository for Embedding model.
"""

from typing import List, Optional, Tuple
from uuid import UUID

import sqlalchemy
from sqlalchemy import Float, cast
from sqlalchemy.orm import Session

from ai_agent.domain.dtos.embedding_dto import EmbeddingCreateDTO
from ai_agent.domain.dtos.search_dto import SearchDTO
from ai_agent.domain.models.database_entities.embedding import Embedding
from ai_agent.infrastructure.database.models.category_model import \
    CategoryModel
from ai_agent.infrastructure.database.models.document_model import \
    DocumentModel
from ai_agent.infrastructure.database.models.embedding_model import \
    EmbeddingModel

from .base_embedding_repository import BaseEmbeddingRepository


class EmbeddingRepository(BaseEmbeddingRepository):
    """
    Concrete implementation of the BaseEmbeddingRepository interface.

    This repository interacts with the 'embeddings' table
    """

    def __init__(self, session: Session):
        """
        Initialize the repository with a session.

        Args:
            session (Session): Active database session.
        """
        self.session = session

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
        embedding_model = EmbeddingModel(
            **data.model_dump(),
            organization_id=organization_id
        )

        self.session.add(embedding_model)
        self.session.commit()
        self.session.refresh(embedding_model)

        return Embedding.model_validate(embedding_model)

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
        query = self.session.query(EmbeddingModel).filter(
            EmbeddingModel.organization_id == organization_id
        )

        if document_id:
            query = query.filter(EmbeddingModel.document_id == document_id)

        if category_id or collection_id:
            query = query.join(EmbeddingModel.document)

            if category_id:
                query = query.filter(DocumentModel.category_id == category_id)

            if collection_id:
                query = query.join(DocumentModel.category)
                query = query.filter(CategoryModel.collection_id == collection_id)

        results = query.all()
        return [Embedding.model_validate(result) for result in results]

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
        query = (
            self.session.query(EmbeddingModel)
            .filter(EmbeddingModel.organization_id == organization_id)
        )

        if document_id:
            query = query.filter(EmbeddingModel.document_id == document_id)

        if category_id or collection_id:
            query = query.join(EmbeddingModel.document)

            if category_id:
                query = query.filter(DocumentModel.category_id == category_id)

            if collection_id:
                query = query.join(DocumentModel.category)
                query = query.filter(CategoryModel.collection_id == collection_id)

        query.delete(synchronize_session=False)
        self.session.commit()

    def search(
        self,
        organization_id: UUID,
        data: SearchDTO
    ) -> List[Tuple[Embedding, float]]:
        """
        Search for similar embeddings based on vector similarity.

        This abstract method defines the interface for performing semantic searches
        against stored embeddings. The search uses vector similarity to find the most
        relevant content based on the provided query vector.

        Args:
            organization_id (UUID): ID of the organization
            data (SearchDTO): The search parameters, including:
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
        # Extract search data
        query_vector: List[float] = data.query_vector
        top_k: int = data.top_k
        document_id: Optional[UUID] = data.document_id
        category_id: Optional[UUID] = data.category_id
        collection_ids: Optional[List[UUID]] = data.collection_ids
        # Define cosine similarity using pgvector's <=> operator
        similarity_expression = cast(EmbeddingModel.embedding.op("<=>")(query_vector), Float)

        # Initialize query to select embedding + similarity score
        query_statement = (
            self.session.query(
                EmbeddingModel,
                similarity_expression.label("distance")
            )
            .filter(EmbeddingModel.organization_id == organization_id)
        )

        # Optional filtering by document
        if document_id:
            query_statement = query_statement.filter(
                EmbeddingModel.document_id == document_id
            )

        # Optional join and filtering by category or collection
        if category_id or collection_ids:
            query_statement = query_statement.join(EmbeddingModel.document)

            if category_id:
                query_statement = query_statement.filter(
                    DocumentModel.category_id == category_id
                )

            if collection_ids:
                query_statement = query_statement.join(DocumentModel.category)
                query_statement = query_statement.where(
                    CategoryModel.collection_id.in_(collection_ids)
                )

        # Execute query and retrieve top-k most similar embeddings
        result_records = (
            query_statement
            .order_by(sqlalchemy.asc("distance"))
            .limit(top_k)
            .all()
        )

        # Convert ORM results to domain models and attach similarity score
        similar_embeddings: List[Tuple[Embedding, float]] = []
        for embedding_orm_model, similarity_score in result_records:
            embedding_domain_model = Embedding.model_validate(embedding_orm_model)
            similar_embeddings.append((embedding_domain_model, similarity_score))

        return similar_embeddings
