"""
Module providing a recursive character-based document splitter.

This module defines the RecursiveSplitter class,
which splits documents into smaller chunks using character-based strategies
with configurable chunk size and overlap parameters.
"""

from typing import List

from langchain.text_splitter import RecursiveCharacterTextSplitter

from ai_agent.domain.value_objects.retrieval_document import RetrievalDocument
from ai_agent.infrastructure.mappers.langchain_document_mapper import (
    convert_from_langchain_documents, convert_to_langchain_documents)

from .base import BaseSplitter


class RecursiveSplitter(BaseSplitter):
    """
    Recursive character document splitter
    """

    def __init__(self, config):
        """
        Initialize the recursive character splitter.

        Args:
            config: a configuration object  with the following attributes:
                chunk_size (int): The maximum number of characters per chunk.
                chunk_overlap (int): The number of characters to overlap between chunks.
        """
        self.splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
        )

    def split_documents(
            self,
            retrieval_documents: List[RetrievalDocument]
        ) -> List[RetrievalDocument]:
        """
        Split a list of documents into smaller chunks.

        Args:
            documents (List[Document]): The input documents to split.

        Returns:
            List[Document]: A list of chunked documents.
        """
        # Convert RetrievalDocument to Langchain Document
        langchain_docs = convert_to_langchain_documents(retrieval_documents)

        # Split Document
        split_lang_docs = self.splitter.split_documents(langchain_docs)

        # Convert to RetrievalDocument
        return convert_from_langchain_documents(split_lang_docs)
