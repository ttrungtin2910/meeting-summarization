"""
This module provides a factory function to obtain a token manager instance.
"""

from fastapi import Depends

from ai_agent.config import JWTConfig
from ai_agent.infrastructure.token_manager.base_token_manager import \
    BaseTokenManager
from ai_agent.infrastructure.token_manager.jwt_token_manager import \
    JWTTokenManager


def get_jwt_config():
    """
    Provides an instance of the JWTTokenManager.

    Returns:
        BaseTokenManager: An instance of `JWTTokenManager` for token management.
    """
    return JWTConfig


def get_token_manager(config = Depends(get_jwt_config)) -> BaseTokenManager:
    """
    Returns an instance of a token manager.

    Returns:
        BaseTokenManager: An instance of `JWTTokenManager`.
    """
    secret_key = config.secret_key
    algorithm = config.algorithm
    expiration_minutes = config.expiration_minutes
    return JWTTokenManager(
        secret_key=secret_key,
        algorithm=algorithm,
        expiration_minutes=expiration_minutes,
    )
