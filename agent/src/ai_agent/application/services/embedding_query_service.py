"""
Query service to search in the vector store
"""

from typing import List, Tuple
from uuid import UUID

from ai_agent.config.config import GraphConfig
from ai_agent.domain.dtos.search_dto import SearchDTO
from ai_agent.domain.exceptions.collection_exceptions import CollectionNotFound
from ai_agent.domain.models.database_entities.embedding import Embedding
from ai_agent.domain.value_objects.retrieval_document import RetrievalDocument
from ai_agent.infrastructure.database.repositories import (
    BaseCollectionRepository, BaseEmbeddingRepository)
from ai_agent.infrastructure.document_embedder.base import BaseEmbedder


class EmbeddingQueryService:
    """
    Service to perform vector search and return retrieval documents from embeddings.
    """
    def __init__(
            self,
            embedding_repository: BaseEmbeddingRepository,
            collection_repository: BaseCollectionRepository,
            embedder: BaseEmbedder
        ):
        """
        Initialize the query service.

        Args:
            embedding_repository (BaseEmbeddingRepository): Handles vector similarity search.
            collection_repository (BaseCollectionRepository):
                Handles operations related to collection table
            embedder (BaseEmbedder): Embeds input text into vector.
        """
        self.embedding_repository = embedding_repository
        self.collection_repository = collection_repository
        self.embedder = embedder

    def search(
            self,
            query_text: str,
            collection_ids: List[UUID],
            organization_id: UUID
        ) -> List[RetrievalDocument]:
        """
        Search for top-k similar embeddings and convert them to RetrievalDocument.

        Args:
            query_text (str): Input query.
            collection_id: ID of the collection to query from
            organization_id: ID of the organization

        Returns:
            List[RetrievalDocument]: List of documents with similarity score.
        """
        # Check if collection exists
        for collection_id in collection_ids:
            if not self.collection_repository.exists(
                collection_id=collection_id,
                organization_id=organization_id
            ):
                raise CollectionNotFound(collection_id=collection_id)

        query_vector = self.embedder.embed_text(query_text)

        search_dto = SearchDTO(
            query_vector=query_vector,
            top_k=GraphConfig.num_chunks,
            collection_ids=collection_ids
        )
        results: List[Tuple[Embedding, float]] = (
            self.embedding_repository
            .search(
                organization_id=organization_id,
                data=search_dto
            )
        )

        retrieval_documents: List[RetrievalDocument] = []

        for embedding, similarity_score in results:
            retrieval_documents.append(
                RetrievalDocument(
                    page_content=embedding.content,
                    metadata={
                        "document_id": str(embedding.document_id),
                        "distance": similarity_score
                    }
                )
            )

        return retrieval_documents
