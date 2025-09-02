"""Chroma vector store database"""

import os
from typing import List

from langchain.schema import Document
from langchain_chroma import Chroma

from .base import BaseVectorStore


class ChromaVectorStorage(BaseVectorStore):
    """
    A vector store implementation using Chroma for document storage and similarity search.

    This class wraps the Chroma library to provide persistent storage of vector embeddings.
    It allows for adding documents and performing similarity-based retrievals based on embeddings.
    """
    def __init__(self, config, embedding_function):
        """
        Initialize the Chroma vector store with configuration settings.

        Args:
            config: A configuration object containing:
                - COLLECTION_NAME (str): Name of the Chroma collection.
                - VECTOR_STORE_ROOT (str): Base directory path for vector store persistence.
                - embedding_function (Callable): Function used to convert documents to embeddings.
            embedding_function: The function used to convert documents to embeddings.
        """
        self.persist_directory = os.path.join(config.VECTOR_STORE_ROOT, config.COLLECTION_NAME)
        if not os.path.exists(self.persist_directory):
            os.makedirs(self.persist_directory)

        self.chroma = Chroma(
            collection_name=config.COLLECTION_NAME,
            embedding_function=embedding_function,
            persist_directory=self.persist_directory
        )

    def add_documents(self, documents: List[Document]):
        """
        Add a list of documents to the Chroma storage.

        Parameters:
            - documents (List[Document]): A list of documents to be added.
        """
        self.chroma.add_documents(documents)

    def similarity_search(self, query: str, k: int = 5):
        """
        Perform a similarity search on the stored documents.

        Parameters:
            - query (str): The query string to search for similar documents.
            - k (int): The number of top similar documents to return. Default is 5.

        Returns:
            - List[Document]: A list of the top k similar documents.
        """
        return self.chroma.similarity_search(query, k=k)

    def as_retriever(self):
        """
        Convert the storage into a retriever object.

        Returns:
            - Retriever: An object that can be used to retrieve documents.
        """
        return self.chroma.as_retriever()

    def delete_documents(self, filters: dict):
        """
        Attempt to delete documents based on metadata filters.

        Parameters:
            - filters (dict): A dictionary of metadata filters to apply for deletion.

        Raises:
            - NotImplementedError: This method is not supported by Chroma.
        """
        raise NotImplementedError("Chroma does not support delete by metadata")

    def get_documents(self, filters: dict):
        """
        Attempt to get documents based on metadata filters.

        Parameters:
            - filters (dict): A dictionary of metadata filters to apply for getting documents.

        Raises:
            - NotImplementedError: This method is not supported by Chroma.
        """
        raise NotImplementedError("Chroma does not support get by metadata.")
