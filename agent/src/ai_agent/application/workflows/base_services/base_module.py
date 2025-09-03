"""
Base module interface for all processing steps.

Each module must implement the `run` method, which processes
the given state and returns the updated state.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseModule(ABC):
    """
    Abstract base class for system modules that process state data.

    All module implementations must inherit from this class and
    implement the run method to ensure consistent state processing.
    """
    @abstractmethod
    async def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the input state and return a modified state.

        Args:
            state (Dict[str, Any]): Current state dictionary with input and previous results.

        Returns:
            Dict[str, Any]: Updated state dictionary with processing results.
        """
