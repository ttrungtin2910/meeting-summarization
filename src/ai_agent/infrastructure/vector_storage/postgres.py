"PostgreSQL vector store database"

import json
import urllib.parse
from typing import List

from langchain.schema import Document
from langchain_postgres import PGVector

from .base import BaseVectorStore


class PostgresVectorStorage(BaseVectorStore):
    """
    A vector store implementation that uses PGVector
    for storing and searching vector embeddings.

    This class provides methods to add documents, perform similarity search,
    and convert the vector store into a retriever for use in RAG pipelines.
    """
    def __init__(self, config, embedding_function, sql_storage):
        """
        Initialize the PostgresVectorStorage instance.

        This method sets up the PGVector-based vector store using the provided configuration,
        embedding function, and SQL storage connection.

        Args:
            config: Configuration object containing connection parameters:
                - user
                - password
                - host
                - port
                - database,
                - collection name
                - use_jsonb
            embedding_function: A function or model used to generate embeddings for documents.
            sql_storage: SQL storage instance used for additional data operations.

        """

        encoded_password = urllib.parse.quote_plus(config.password)
        connection_string = f"postgresql+psycopg://{config.user}:{encoded_password}@{config.host}:\
            {config.port}/{config.database}"

        self.vector_store = PGVector(
            collection_name=config.collection_name,
            connection=connection_string,
            embeddings=embedding_function,
            use_jsonb=config.use_jsonb,
        )
        self.sql_storage = sql_storage
        self.collection_name = config.collection_name

    def add_documents(self, documents: List[Document]):
        """
        Add a list of LangChain Document objects to the vector store.

        Args:
            documents (List[Document]): The documents to add, each with content and metadata.
        """
        self.vector_store.add_documents(documents)

    def similarity_search(self, query: str, k: int = 5):
        """
        Perform a similarity search in the vector store.

        Args:
            query (str): The natural language query to search for.
            k (int): The number of most similar documents to return.

        Returns:
            List[Document]: A list of documents ranked by similarity to the query.
        """
        return self.vector_store.similarity_search(query, k=k)

    def as_retriever(self):
        """
        Convert the vector store into a retriever interface.

        Returns:
            BaseRetriever: A retriever instance that can be used in LangChain pipelines.
        """
        return self.vector_store.as_retriever()

    def delete_documents(self, filters: dict):
        """
        Delete documents from the PGVector storage that match the given metadata filters.

        Args:
            filters (Dict[str, str]): Dictionary of metadata key-value pairs to filter on.
        """
        conditions = [f"cmetadata->>%(key_{i})s = %(value_{i})s" for i in range(len(filters))]
        sql = (
            f"DELETE FROM langchain_pg_embedding "
            f"WHERE collection_id IN ("
            f"  SELECT uuid FROM langchain_pg_collection WHERE name = %(collection_name)s"
            f") AND {' AND '.join(conditions) if conditions else 'TRUE'}"
        )
        params = {"collection_name": self.collection_name}
        for i, (k, v) in enumerate(filters.items()):
            params[f"key_{i}"] = k
            params[f"value_{i}"] = v
        return self.sql_storage.execute(sql, params)

    def get_documents(self, filters: dict):
        """
        Get documents from the PGVector storage that match the given metadata filters.

        Args:
            filters (Dict[str, str]): Dictionary of metadata key-value pairs to filter on.
        """
        conditions = [f"cmetadata->>%(key_{i})s = %(value_{i})s" for i in range(len(filters))]
        sql = (
            f"SELECT DISTINCT cmetadata->> 'filename', cmetadata->> 'category' "
            f"FROM langchain_pg_embedding "
            f"WHERE collection_id IN ("
            f"  SELECT uuid FROM langchain_pg_collection WHERE name = %(collection_name)s"
            f") AND {' AND '.join(conditions) if conditions else 'TRUE'}"
        )
        params = {"collection_name": self.collection_name}
        for i, (k, v) in enumerate(filters.items()):
            params[f"key_{i}"] = k
            params[f"value_{i}"] = v
        return self.sql_storage.execute(sql, params)

    def update_metadata(self, original_filters: dict, updates: dict):
        """
        Update metadata fields of documents in PGVector storage that match the given filters.

        Args:
            original_filters (Dict[str, str]): Dictionary of metadata key-value pairs to identify
                                            the documents to update.
            updates (Dict[str, str]): Dictionary of metadata fields and their new values
                                    to be updated.

        Returns:
            int: Number of documents updated.
        """
        if not updates:
            raise ValueError("Updates dictionary cannot be empty")

        # Build filter conditions using proper parameterization
        filter_conditions = [f"cmetadata->>%(key_{i})s = %(value_{i})s"
                            for i in range(len(original_filters))]

        # Start with the base cmetadata
        update_sql_part = "cmetadata"

        # Build the nested jsonb_set calls correctly
        for field in updates:
            # Use the correct syntax for the JSON path: '{field}'
            update_sql_part = f"jsonb_set({update_sql_part}, '{{{field}}}', \
                %(update_{field})s::jsonb, true)"

        # Build the final SQL query
        sql = (
            f"UPDATE langchain_pg_embedding "
            f"SET cmetadata = {update_sql_part} "
            f"WHERE collection_id IN ("
            f"  SELECT uuid FROM langchain_pg_collection WHERE name = %(collection_name)s"
            f") AND {' AND '.join(filter_conditions) if filter_conditions else 'TRUE'}"
        )

        # Prepare parameters
        params = {"collection_name": self.collection_name}

        # Add filter parameters
        for i, (k, v) in enumerate(original_filters.items()):
            params[f"key_{i}"] = k
            params[f"value_{i}"] = v

        # Add update parameters with proper JSON formatting
        for field, value in updates.items():
            # Convert value to JSON string
            params[f"update_{field}"] = json.dumps(value)

        return self.sql_storage.execute(sql, params)
