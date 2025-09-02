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
    agent_name = "RIA User Guide Helper"

    # Description helps to detect the topics can be supported and out-out-scope topics
    system_description = """Websites: https://admin.eu.ia.ricoh.com/admin.html, https://admin.na.ia.ricoh.com/admin.html, and https://admin.ap.ia.ricoh.com/admin.html
Ricoh Intelligent Automation (RIA) automates the extraction, validation, and organization of data from both digital and physical documents. RIA integrates with AI solutions such as Natif AI and Azure AI to enhance data extraction, validation, and tagging in various formats.

Key features and process steps include:
- Pre-processing scanned documents to optimize accuracy (splitting, cropping, etc.)
- Intelligent document classification for tagging and context recognition
- Automated data extraction to retrieve all required values from documents
- Domain-specific validation to apply extracted data to the relevant forms or systems
- Human-in-the-loop validation (Work Queue) for improved machine learning accuracy

RIA is designed for organizations with high document processing needs, such as healthcare clinics, financial institutions, and business offices. With RIA, clinics, for example, can seamlessly digitize and organize vital patient information, ensuring fast and secure access for healthcare providers.

To access RIA's Operations portal, use the region-specific URLs above. Supported browsers include Google Chrome, Mozilla Firefox, and Microsoft Edge.
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
    num_chunks: int = 20


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
