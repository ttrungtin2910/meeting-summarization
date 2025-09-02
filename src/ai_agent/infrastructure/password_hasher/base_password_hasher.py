"""
Defines an abstract base class for password hashing.
"""

from abc import ABC, abstractmethod


class BasePasswordHasher(ABC):
    """
    Interface for hashing and verifying passwords.
    """

    @abstractmethod
    def hash(self, password: str) -> str:
        """
        Hash a plain password.

        Args:
            password (str): Raw password.

        Returns:
            str: Hashed password.
        """

    @abstractmethod
    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a plain password against its hashed version.

        Args:
            plain_password (str): Raw input password.
            hashed_password (str): Stored hashed password.

        Returns:
            bool: Whether the password matches.
        """
