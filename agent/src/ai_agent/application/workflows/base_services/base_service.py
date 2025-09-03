"""
Base service class to standardize running a pipeline service.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict

from .pipeline import Pipeline


class BaseService(ABC):
    """
    Abstract base class for any pipeline service.
    """
    def __init__(self):
        """
        Initialize the service by building the pipeline.
        """
        self.pipeline = self.build_pipeline()

    @abstractmethod
    def build_pipeline(self) -> Pipeline:
        """
        Build and return the pipeline for this service.

        Returns:
            BasePipeline: The constructed pipeline.
        """

    async def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the service with the given state.

        Args:
            state (Dict[str, Any]): The input state.

        Returns:
            Dict[str, Any]: The output state after processing.
        """
        return await self.pipeline.run(state)
