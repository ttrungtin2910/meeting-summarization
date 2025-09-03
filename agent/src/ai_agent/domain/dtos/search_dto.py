"""
Search Request DTO
"""

from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class SearchRequestDTO(BaseModel):
    """
    Data Transfer Object for initiating a search request, from API to Application.

    Args:
        query_vector (List[float]): The input embedding vector for similarity search.
        top_k (int): Number of top similar results to return.
        document_id (Optional[UUID]): Limit search to a specific document.
        category_id (Optional[UUID]): Limit search to a specific category.
        collection_id (Optional[UUID]): Limit search to a specific collection.
    """
    query_vector: List[float]
    top_k: int
    document_id: Optional[UUID] = None
    category_id: Optional[UUID] = None
    collection_id: Optional[UUID] = None


class SearchDTO(BaseModel):
    """
    Data Transfer Object for search parameters, from Application to Repository.

    Args:
        query_vector (List[float]): The input embedding vector for similarity search.
        top_k (int): Number of top similar results to return.
        document_id (Optional[UUID]): Limit search to a specific document.
        category_id (Optional[UUID]): Limit search to a specific category.
        collection_ids (Optional[List[UUID]]): Limit search to specific collections.
    """
    query_vector: List[float]
    top_k: int
    document_id: Optional[UUID] = None
    category_id: Optional[UUID] = None
    collection_ids: Optional[List[UUID]] = None

    class Config:
        """Config for mapping data"""
        from_attributes = True
