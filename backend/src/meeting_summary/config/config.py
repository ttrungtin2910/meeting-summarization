"""Configuration for Meeting Summary project"""

import os
from dataclasses import dataclass
from typing import List

from pydantic import SecretStr


class APIConfig:
    """Config for API module"""
    def __init__(self):
        origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000")
        self.allow_origins = origins.split(",")


@dataclass(frozen=True)
class OpenAIConfig:
    """Config for OpenAI API"""
    api_key: SecretStr = SecretStr(os.getenv("OPENAI_API_KEY", ""))
    model: str = "whisper-1"  # Speech-to-text model
    language: str = "vi"  # Vietnamese language
    
    # For text summarization
    chat_model: str = "gpt-4o-mini"
    temperature: float = 0.3


@dataclass(frozen=True)
class JWTConfig:
    """Config for JWT service"""
    secret_key: str = os.getenv("JWT_SECRET_KEY", "your-secret-key-here")
    algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    expiration_minutes: int = 300


# Initialize config instances
api_config = APIConfig()
openai_config = OpenAIConfig()
jwt_config = JWTConfig()
