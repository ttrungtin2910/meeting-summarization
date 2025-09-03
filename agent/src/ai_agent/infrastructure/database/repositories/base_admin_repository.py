"""
Defines the abstract base repository interface for working with Admin entities.
"""

from abc import ABC, abstractmethod
from typing import Optional

from ai_agent.domain.models.database_entities.admin import Admin


class BaseAdminRepository(ABC):
    """
    Abstract base class for Admin repository.
    """

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Admin]:
        """
        Retrieves an Admin entity by their email address.

        Args:
            email (str): The email address of the Admin to retrieve.

        Returns:
            Optional[Admin]: The Admin entity if found, otherwise None.
        """
