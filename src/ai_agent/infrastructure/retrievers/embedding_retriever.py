"""
Custom Retriever Module for Semantic Search.

This module provides a custom implementation of LangChain's BaseRetriever
that enables semantic search using vector embeddings
"""

from typing import List
from uuid import UUID

from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever

from ai_agent.application.services.embedding_query_service import \
    EmbeddingQueryService


class EmbeddingRetriever(BaseRetriever):
    """
    A retriever that performs semantic search using vector embeddings.

    This retriever implements LangChain's BaseRetriever interface to enable
    semantic search capabilities in AI agent workflows

    Attributes:
        embedding_query_service (EmbeddingQueryService):
            Service that performs vector similarity search
    """

    embedding_query_service: EmbeddingQueryService

    class Config:
        """
        Configuration for the EmbeddingRetriever model.

        This configuration allows the model to accept arbitrary Python types
        as field values, which is necessary for complex objects like the
        EmbeddingQueryService that might not be directly serializable.
        """
        arbitrary_types_allowed = True

    def _get_relevant_documents(
            self,
            query: str,
            *,
            run_manager=None,
            **kwargs,
        ) -> List[Document]:
        """
        Retrieves relevant documents based on a query string and specified identifiers.

        This method uses the embedding query service to search for documents
        that match the given query within a specified collection and organization.
        It ensures that the collection and organization IDs
        are valid UUIDs before proceeding with the search.

        Parameters:
            query (str): The query string used to search for relevant documents.
            run_manager (optional): An optional parameter for managing
                the execution context or state.
            **kwargs: Additional keyword arguments that may include:
                - collection_ids (List[UUID]): The ID of the collection to search within.
                - organization_id (UUID): The ID of the organization associated with the search.

        Returns:
            List[Document]: A list of Document objects containing the page content
                and metadata of the retrieved documents.

        Raises:
            ValueError: If either collection_id or organization_id is not a valid UUID.
        """
        collection_ids = kwargs.get("collection_ids")
        organization_id = kwargs.get("organization_id")

        if any([not isinstance(collection_id, UUID) for collection_id in collection_ids]):
            raise ValueError("collection_id must be a UUID")

        if not isinstance(organization_id, UUID):
            raise ValueError("organization_id must be a UUID")

        retrieval_docs = self.embedding_query_service.search(
            query_text=query,
            collection_ids=collection_ids,
            organization_id=organization_id,
        )
        return [
            Document(page_content=doc.page_content, metadata=doc.metadata)
            for doc in retrieval_docs
        ]
