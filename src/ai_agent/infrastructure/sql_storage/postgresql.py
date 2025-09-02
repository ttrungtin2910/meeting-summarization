"""
PostgreSQL implementation of the SQL storage interface.
"""

from contextlib import contextmanager
from typing import Any, Dict, List, Optional, Tuple, Union

import psycopg2

from .base import BaseSQLStorage


class PostgreSQLStorage(BaseSQLStorage):
    """
    PostgreSQL implementation of the SQL storage interface with minimal design.
    Focuses on providing a execute method and session management.
    """

    def __init__(self, config):
        """
        Initialize PostgreSQL connection with configuration.

        Args:
            config: Configuration object containing PostgreSQL connection parameters:
                - database: Database name
                - user: Username
                - password: Password (masked in the example)
                - host: Host address
                - port: Port number
        """
        self.connection_string = f"dbname={config.database} user={config.user} \
            password={config.password} host={config.host} port={config.port}"

    def execute(self, query: str,
                params: Optional[Union[Dict[str, Any], List[Any], Tuple[Any]]] = None) -> Any:
        """
        Execute a SQL query with optional parameters and return the results.

        Args:
            query: SQL query string to execute
            params: Parameters to bind to the query

        Returns:
            Any: For SELECT queries, returns query results
                For INSERT/UPDATE/DELETE, returns affected row count

        Raises:
            Exception: If the query fails to execute
        """
        with self.get_db() as session:
            cursor = None
            try:
                cursor = session.cursor()
                cursor.execute(query, params)

                # Check if this is a SELECT query (which returns results)
                if query.strip().upper().startswith("SELECT"):
                    results = cursor.fetchall()
                    return results
                else:
                    # For non-SELECT queries, return row count
                    session.commit()
                    return cursor.rowcount

            except Exception:
                session.rollback()
                raise
            finally:
                if cursor:
                    cursor.close()

    @contextmanager
    def get_db(self):
        """
        Get a database connection to work with.

        This method provides a context manager that yields a database connection.
        The connection is automatically closed when exiting the context.

        Yields:
            A database connection object

        Raises:
            ConnectionError: If connection cannot be established

        Usage:
            with storage.get_db() as session:
                # Use session for database operations
                cursor = session.cursor()
                cursor.execute("SELECT * FROM users")
                result = cursor.fetchall()
        """
        connection = None
        try:
            connection = psycopg2.connect(self.connection_string)
            connection.autocommit = False
            yield connection
            connection.commit()
        except Exception:
            if connection:
                connection.rollback()
            raise
        finally:
            if connection:
                connection.close()
