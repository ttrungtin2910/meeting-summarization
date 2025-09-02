"""
This module defines the BaseTokenManager interface for token management.
"""

from abc import ABC, abstractmethod
from typing import Optional


class BaseTokenManager(ABC):
    """
    Interface for token management, providing methods to encode and decode tokens.
    """

    @abstractmethod
    def encode(self, data: dict) -> str:
        """
        Encodes data into a token.

        Args:
            data (dict): The data to be encoded into the token.

        Returns:
            str: The encoded token as a string.
        """

    @abstractmethod
    def decode(self, token: str) -> Optional[dict]:
        """
        Decodes a token back into data.

        Args:
            token (str): The token to be decoded.

        Returns:
            dict: The decoded data from the token, None if malformed or expired token
        """
