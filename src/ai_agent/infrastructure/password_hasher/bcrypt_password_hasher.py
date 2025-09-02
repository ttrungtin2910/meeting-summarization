"""
Implementation of PasswordHasher using bcrypt via passlib.
"""

from passlib.context import CryptContext

from ai_agent.infrastructure.password_hasher.base_password_hasher import \
    BasePasswordHasher


class BcryptPasswordHasher(BasePasswordHasher):
    """
    Implementation of PasswordHasher using bcrypt.
    """

    def __init__(self):
        self._context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash(self, password: str) -> str:
        """
        Hash a plain password using bcrypt.

        Args:
            password (str): Raw password to hash.

        Returns:
            str: Bcrypt hashed password.
        """
        return self._context.hash(password)

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a plain password against its hashed version.

        Args:
            plain_password (str): Raw input password.
            hashed_password (str): Hashed password from storage.

        Returns:
            bool: True if password matches, False otherwise.
        """
        return self._context.verify(plain_password, hashed_password)
