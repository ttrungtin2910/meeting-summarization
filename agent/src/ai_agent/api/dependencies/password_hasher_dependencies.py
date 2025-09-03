"""
This module provides a dependency for password hashing using the hashing
algorithm.
"""

from ai_agent.infrastructure.password_hasher.base_password_hasher import \
    BasePasswordHasher
from ai_agent.infrastructure.password_hasher.bcrypt_password_hasher import \
    BcryptPasswordHasher


def get_password_hasher() -> BasePasswordHasher:
    """
    Dependency provider for PasswordHasher using bcrypt.

    Returns:
        PasswordHasher: Instance of BcryptPasswordHasher.
    """
    return BcryptPasswordHasher()
