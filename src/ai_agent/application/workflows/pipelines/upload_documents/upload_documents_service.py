"""
Service to run the Upload Documents pipeline.
"""

import os

from ai_agent.application.workflows.base_services import (
    BaseService, Pipeline, load_pipeline_from_yaml)
from ai_agent.infrastructure.document_splitter import get_splitter
from ai_agent.infrastructure.vector_storage import get_vector_storage


class UploadDocumentsService(BaseService):
    """
    Upload Documents Service

    This service processes text files by uploading, splitting, and saving document chunks.

    Pipeline modules are defined in config.yaml.

    State Requirements:

    Input State (Dict[str, Any]):
    - file_paths (List[str]): List of text file paths to process.
    - category (Optional[str]): Category label for the documents.

    Output State (Dict[str, Any]):
    - documents (List): Loaded Document objects.
    - chunks (List): Split document chunks ready for storage.
    """
    def build_pipeline(self) -> Pipeline:
        """
        Build the Upload Documents pipeline.

        Returns:
            BasePipeline: The constructed pipeline.
        """
        # Initialize dependencies
        splitter = get_splitter()
        vector_storage = get_vector_storage()
        init_args = {
            "splitter": splitter,
            "vector_storage": vector_storage,
        }

        # Read configuration file
        yaml_path = os.path.join(
            os.path.dirname(__file__), "config.yaml"
        )

        # Load pipeline
        return load_pipeline_from_yaml(os.path.abspath(yaml_path), init_args=init_args)
