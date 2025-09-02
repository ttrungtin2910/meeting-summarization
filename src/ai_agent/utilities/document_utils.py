"""Utilities for process Document"""

import os
from datetime import datetime
from typing import Optional

from langchain.schema import Document


def convert_text_file_to_documents(path: str, category: Optional[str] = None) -> Document:
    """
    Convert a text file to Document objects with metadata.

    Args:
        path: Path to the text file
        category: Category label for the document

    Returns:
        Document object with text content and metadata
    """

    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    filename = os.path.basename(path).split(".")[0]
    # Get file creation and modification times
    current_time = datetime.now().isoformat()

    metadata = {
        "filename": filename,
        "category": category,
        "created_at": current_time,
        "modified_at": current_time
    }
    return Document(page_content=text, metadata=metadata)
