"""
Document Sync Service Module.
"""

import tempfile
from datetime import datetime, timezone
from typing import List
from uuid import UUID

from ai_agent.domain.dtos.document_dto import DocumentUpdateDTO
from ai_agent.domain.dtos.embedding_dto import EmbeddingCreateDTO
from ai_agent.domain.dtos.sync_dto import SyncResponseDTO
from ai_agent.domain.exceptions.collection_exceptions import CollectionNotFound
from ai_agent.domain.models.database_entities.document import Document
from ai_agent.domain.models.security_contexts.organization_context import \
    OrganizationContext
from ai_agent.domain.value_objects.document_status import DocumentStatus
from ai_agent.domain.value_objects.retrieval_document import RetrievalDocument
from ai_agent.infrastructure.database.repositories import (
    BaseCollectionRepository, BaseDocumentRepository, BaseEmbeddingRepository,
    BaseOrganizationRepository)
from ai_agent.infrastructure.document_embedder.base import BaseEmbedder
from ai_agent.infrastructure.document_splitter.base import BaseSplitter
from ai_agent.infrastructure.storage.base import BaseStorage
from ai_agent.utilities.file_utils import delete_file


class DocumentSyncService:
    """
    Service to synchronize embeddings based on document status.

    This service manages the synchronization process between document storage and vector embeddings.
    It processes documents based on their status, handles deletion, updates, and creation of
    embeddings, and ensures consistency between the document repository and the vector store.
    """

    def __init__(
        self,
        document_repository: BaseDocumentRepository,
        embedding_repository: BaseEmbeddingRepository,
        collection_repository: BaseCollectionRepository,
        organization_repository: BaseOrganizationRepository,
        storage: BaseStorage,
        splitter: BaseSplitter,
        embedder: BaseEmbedder,
    ):
        """
        Initialize the DocumentSyncService with required dependencies.

        Args:
            organization_repository (BaseOrganizationRepository): repository for organization table
            storage (BaseStorage): Storage service for file operations
            splitter (BaseSplitter): Service to split documents into chunks
            embedder (BaseEmbedder): Service to generate vector embeddings
        """
        self.organization_repository = organization_repository
        self.document_repository = document_repository
        self.embedding_repository = embedding_repository
        self.collection_repository = collection_repository
        self.storage = storage
        self.splitter = splitter
        self.embedder = embedder

    def sync_documents(
            self,
            collection_id: UUID,
            organization_context: OrganizationContext,
        ) -> SyncResponseDTO:
        """
        Synchronize documents in a collection based on their current status.

        This method processes all documents in a collection and takes appropriate actions based on
        their status:
        - EMBEDDED: Skip as they're already processed
        - DELETED: Remove from both document storage and embedding storage
        - UPDATED: Remove old embeddings and re-embed
        - PENDING: Process for embedding

        Args:
            collection_id (UUID): The ID of the collection to synchronize
            organization_context (OrganizationContext): The authenticated client

        Returns:
            None
        """
        # Check if collection exists:
        organization_id = organization_context.organization_id
        collection = self.collection_repository.get_by_id(
            collection_id=collection_id,
            organization_id=organization_id
        )
        if not collection:
            raise CollectionNotFound(collection_id=collection_id)

        # Variables to store statistical information
        added = 0
        deleted = 0
        updated = 0

        # Get list of documents belongs to the organization/collection
        database_documents = self.document_repository.get_list(
            organization_id=organization_id,
            collection_id=collection_id
        )
        documents_to_embed: List[Document] = []

        # Find which documents need to embed or delete
        for document in database_documents:
            match document.status:
                case DocumentStatus.EMBEDDED:
                    continue

                case DocumentStatus.DELETED:
                    deleted += 1
                    self.embedding_repository.delete(
                        organization_id=organization_id,
                        document_id=document.id
                    )
                    self.document_repository.delete(
                        document.id,
                        organization_id=organization_id
                    )

                case DocumentStatus.UPDATED:
                    updated += 1
                    # Delete current embedding
                    self.embedding_repository.delete(
                        document_id=document.id,
                        organization_id=organization_id
                    )
                    # Embed new document
                    documents_to_embed.append(document)

                case DocumentStatus.PENDING:
                    added += 1
                    documents_to_embed.append(document)

        # Embed documents
        if len(documents_to_embed) > 0:
            self._embed_documents(
                documents_to_embed,
                organization_id=organization_id
            )

        return SyncResponseDTO(
            added=added,
            deleted=deleted,
            updated=updated
        )

    def _embed_documents(
            self,
            documents: List[Document],
            organization_id: UUID,
        ) -> None:
        """
        Process documents for embedding.

        This method orchestrates the embedding process by downloading,
        reading, splitting, and embedding documents.

        Args:
            documents (List[Document]): List of documents to process for embedding.
            organization_id (UUID): ID of the organization

        Returns:
            None
        """
        # Download and read documents
        retrieval_docs: List[RetrievalDocument] = self._download_and_read_documents(
            documents,
            organization_id=organization_id
        )
        # Split documents into chunks
        splitted_docs: List[RetrievalDocument] = self.splitter.split_documents(retrieval_docs)
        # Embed and save the document chunks
        self._embed_and_save(splitted_docs, organization_id=organization_id)

    def _download_and_read_documents(
            self,
            documents: List[Document],
            organization_id: UUID,
        ) -> List[RetrievalDocument]:
        """
        Download and read the content of documents.

        This function downloads each document from storage, reads its content,
        and updates the document status to embedded.

        Args:
            documents (List[Document]): List of documents to process.
            organization_id (UUID): ID of the organization

        Returns:
            List[RetrievalDocument]: List of retrieval documents with content and metadata.
        """
        all_retrieval_docs: List[RetrievalDocument] = []

        for document in documents:
            # Generate a temporary file
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_path = temp_file.name

            # Download from remote to temporary file
            self.storage.download(document.storage_uri, temp_path)

            # Read the content
            with open(temp_path, "r", encoding="utf-8") as file:
                content: str = file.read()

            # Delete the temp file
            delete_file(temp_path)

            retrieval_doc = RetrievalDocument(
                page_content=content,
                metadata={"document_id": document.id}
            )
            all_retrieval_docs.append(retrieval_doc)

            # Mark document as embedded
            update_dto = DocumentUpdateDTO(status=DocumentStatus.EMBEDDED)
            self.document_repository.update(
                document.id,
                update_dto,
                organization_id=organization_id
            )

        return all_retrieval_docs

    def _embed_and_save(
            self,
            splitted_docs: List[RetrievalDocument],
            organization_id: UUID,
        ) -> None:
        """
        Generate embeddings and save them.

        This function generates embeddings for each document chunk and saves them to the repository.

        Args:
            splitted_docs (List[RetrievalDocument]): List of split retrieval documents.
            organization_id (UUID): ID of the organization

        Returns:
            None
        """
        # Extract text content from each document chunk
        texts = [doc.page_content for doc in splitted_docs]
        # Generate embeddings for the text content
        vectors = self.embedder.embed_texts(texts)

        for chunk, vector in zip(splitted_docs, vectors):
            dto = EmbeddingCreateDTO(
                document_id=chunk.metadata["document_id"],
                content=chunk.page_content,
                embedding=vector,
                created_at=datetime.now(tz=timezone.utc)
            )
            # Save the embedding to the repository
            self.embedding_repository.create(dto, organization_id=organization_id)
