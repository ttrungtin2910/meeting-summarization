"""
Module to save document chunks into the vector database.
"""

from typing import Any, Dict

from ai_agent.application.workflows.base_services.base_module import BaseModule


class AddChunks(BaseModule):
    """
    Save document chunks into a vector database.
    """
    def __init__(self, vector_storage):
        """
        Initialize SaveChunks with a vector storage.

        Args:
            vector_storage: Storage backend for document chunks.
        """
        self.vector_storage = vector_storage

    async def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Save document chunks to the vector database.

        Args:
            state (Dict[str, Any]): The current pipeline state.

        Returns:
            Dict[str, Any]: State unchanged after saving.
        """
        chunks = state["chunks"]
        self.vector_storage.add_documents(chunks)
        return state
