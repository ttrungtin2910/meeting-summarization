"""
Base interface for language models.

Defines the BaseLanguageModel abstract class for retrieving initialized LLM instances.
"""

from abc import ABC, abstractmethod


class BaseLanguageModel(ABC):
    """
    Interface for language models.
    """
    @abstractmethod
    def get_model(self):
        """Return the initialized LLM instance"""
