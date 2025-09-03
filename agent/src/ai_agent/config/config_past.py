"""Configuration for AI agent project"""

import os
from dataclasses import dataclass
from typing import ClassVar, Dict

from pydantic import SecretStr


@dataclass(frozen=True)
class APIConfig:
    """Config for API module"""
    # List of allowed origins for CORS
    allow_origins = ["*"]


@dataclass(frozen=True)
class VectorStoreConfig:
    """Config for graph"""
    # Storage type
    provider = "postgresql"
    driver = "psycopg2"

    user = os.getenv("SQL_USER", "")
    password = os.getenv("SQL_PASSWORD", "")
    host = os.getenv("SQL_HOST", "")
    port = os.getenv("SQL_PORT", "")
    database = os.getenv("SQL_DATABASE", "")

    use_jsonb = True


@dataclass(frozen=True)
class GraphConfig:
    """Config for graph"""
    # Agent name
    agent_name = "Tony Healthcare Center Assistant"

    # Description helps to detect the topics can be supported and out-out-scope topics
    system_description = """Website: https://hospital.example.com
This chatbot system is designed to assist patients, visitors, and hospital staff by providing information and guidance related to hospital services, procedures, and general healthcare topics.
Supported topics include:
- Hospital departments and contact information
- Outpatient and inpatient services
- Appointment booking and scheduling procedures
- Visiting hours and policies
- Health checkup packages
- Information on hospital facilities (pharmacy, cafeteria, parking, etc.)
- Insurance and billing guidance
- Health education and preventive care tips
- Guidance on pre- and post-treatment care
The chatbot does **not** provide medical diagnoses or emergency medical advice. For urgent medical needs, please contact the hospital hotline or go to the emergency department.
Questions unrelated to hospital services or general healthcare (such as legal, financial, or technical IT support, weather, document extraction) are out of scope.
    """

    # Name of nodes
    nodes = {
        "DETECT_INTENT": "detect_intent",
        "RETRIEVE": "retrieve",
        "GENERATE_CHITCHAT": "generate_chitchat",
        "GENERATE_RAG": "generate_rag",
        "INVALID": "invalid",
        "OUT_OF_SCOPE": "out_of_scope",
        "REPHRASE": "rephrase",
        "SUMMARIZE": "summarize"
    }

    # List of actions like create parsing rule
    actions: ClassVar[Dict[str, str]] = {}

    # Number of chunks to query
    num_chunks: int = 5


@dataclass(frozen=True)
class LLMConfig:
    """Config for LLM object"""
    provider= "azure"

    # Config for LLM API
    api_key: SecretStr = SecretStr(os.getenv("AZURE_OPENAI_API_KEY", ""))
    api_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_version = "2024-08-01-preview"

    # Config for model
    model = "gpt-4o-mini"
    temperature = 0


@dataclass(frozen=True)
class EmbeddingConfig:
    """Config for the embedding function"""
    provider = "azure"
    api_key: SecretStr = SecretStr(os.getenv("EMBEDDING_KEY", ""))
    endpoint: str = os.getenv("EMBEDDING_ENDPOINT", "")
    version = "2024-02-01"
    model = "text-embedding-3-small"


@dataclass(frozen=True)
class StorageConfig:
    """Config for storage service like azure blob"""
    storage_type = "azure"
    account_name = os.getenv("AZURE_ACCOUNT_NAME", "")
    account_key = os.getenv("AZURE_ACCOUNT_KEY", "")
    container_name = "persistance"
    expire_minutes = 60


@dataclass(frozen=True)
class SplitterConfig:
    """Config for document splitter"""
    provider = "recursive_character_text_splitter"
    chunk_size = 200
    chunk_overlap = 50


@dataclass(frozen=True)
class JWTConfig:
    """Config for JWT service"""
    secret_key = os.getenv("JWT_SECRET_KEY", "")
    algorithm = os.getenv("JWT_ALGORITHM", "")
    expiration_minutes = 300
