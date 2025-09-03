"""
Module to split Document objects into smaller chunks.
"""

from typing import Any, Dict

from ai_agent.application.workflows.base_services.base_module import BaseModule


class SplitDocuments(BaseModule):
    """
    Split documents into smaller chunks.
    """

    def __init__(self, splitter):
        """
        Initialize the SplitDocuments module.

        Args:
            splitter: A splitter object capable of splitting documents.
        """
        self.splitter = splitter

    async def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Split the documents into smaller chunks.

        Args:
            state (Dict[str, Any]): The current pipeline state.

        Returns:
            Dict[str, Any]: Updated state with document chunks.
        """
        documents = state["documents"]
        chunks = self.splitter.split_documents(documents)
        state["chunks"] = chunks
        return state
