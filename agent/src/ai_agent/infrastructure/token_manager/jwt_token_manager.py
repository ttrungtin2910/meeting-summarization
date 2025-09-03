"""
This module implements the BaseTokenManager interface using JWT from the
python-jose library.

The JWTTokenManager class provides methods to encode and decode tokens,
leveraging JWT for secure data handling.
"""

from datetime import datetime, timedelta, timezone
from typing import Dict, Optional

from jose import ExpiredSignatureError, JWTError, jwt

from .base_token_manager import BaseTokenManager


class JWTTokenManager(BaseTokenManager):
    """
    JWT-based implementation of the BaseTokenManager.
    """

    def __init__(
            self,
            secret_key: str,
            algorithm: str = "HS256",
            expiration_minutes: int = 30
        ):
        """
        Initializes the JWTTokenManager with a secret key, algorithm, and token expiration time.

        Args:
            secret_key (str): The secret key used for encoding and decoding tokens.
            algorithm (str): The algorithm used for JWT encoding. Default is "HS256".
            expiration_minutes (int): The expiration time for tokens in minutes.
                Default is 30 minutes.
        """
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expiration_minutes = expiration_minutes

    def encode(self, data: Dict) -> str:
        """
        Encodes data into a JWT token.

        Args:
            data (Dict): The data to be encoded into the token.

        Returns:
            str: The encoded JWT token as a string.
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.expiration_minutes)

        # Add expire time
        to_encode.update(
            {"exp": expire}
        )

        encoded_jwt = jwt.encode(
            to_encode,
            self.secret_key,
            algorithm=self.algorithm
        )
        return encoded_jwt

    def decode(self, token: str) -> Optional[Dict]:
        """
        Decodes a JWT token back into data.

        Args:
            token (str): The JWT token to be decoded.

        Returns:
            Dict: The decoded data from the token, None if malformed or expired token
        """
        try:
            decoded_data = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            return decoded_data
        except (JWTError, ExpiredSignatureError):
            return None
