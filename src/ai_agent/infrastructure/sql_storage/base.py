"""
Base interface for SQL storage services.

Defines the BaseSQLStorage abstract class for standardizing
SQL database operations across different backend implementations.
"""

from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Any, Dict, List, Optional, Tuple, Union


class BaseSQLStorage(ABC):
    """
    Abstract base class defining the interface for SQL storage implementations.
    All SQL database adapters should inherit from this class.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the SQL storage with configuration.

        Args:
            config: Dictionary containing connection configuration parameters
        """

    @abstractmethod
    def execute(self, query: str, params: Optional[Union[Dict[str, Any], List[Any], Tuple[Any]]] = None) -> Any:
        """
        Execute a SQL query with optional parameters.

        Args:
            query: SQL query string to execute
            params: Parameters to bind to the query

        Returns:
            Result of the query execution

        Raises:
            QueryExecutionError: If the query fails to execute
        """

    @abstractmethod
    @contextmanager
    def get_db(self):
        """
        Get a database session to work with.

        Yields:
            A session object for executing queries

        Raises:
            ConnectionError: If session cannot be created
        """
