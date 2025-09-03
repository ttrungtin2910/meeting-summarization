"""
Module to load text files into Document objects with metadata.
"""

from typing import Any, Dict

from ai_agent.application.workflows.base_services.base_module import BaseModule
from ai_agent.utilities.document_utils import convert_text_file_to_documents
from ai_agent.utilities.file_utils import delete_file


class LoadDocuments(BaseModule):
    """
    Load text files into Document objects.
    """

    async def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Args:
            state (Dict[str, Any]): Current pipeline state.

        Returns:
            Dict[str, Any]: Updated state.
        """
        file_paths = state["file_paths"]
        category = state.get("category", "default")

        documents = []
        for path in file_paths:
            docs = convert_text_file_to_documents(path, category)
            documents.extend(docs)
            delete_file(path)

        state["documents"] = documents
        return state
