"""
Retrieval Document Module.

This module defines the schema for representing document objects used in graph-based
retrieval operations. It provides a structured format for storing document content
along with its associated metadata.
"""

from typing import Any, Dict

from pydantic import BaseModel


class RetrievalDocument(BaseModel):
    """
    Represents a Document object to be used in graph.

    Attributes:
        page_content (str): The text content of the document.
        metadata (Dict[str, Any]): Associated metadata.
    """
    page_content: str
    metadata: Dict[str, Any]
