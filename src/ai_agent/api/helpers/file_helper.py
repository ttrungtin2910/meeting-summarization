"""Utility functions for files"""

import os
import tempfile
import uuid

from fastapi import UploadFile


async def save_temp_file(file: UploadFile) -> str:
    """
    Save an uploaded file to a temporary location on disk.

    This function receives an UploadFile from FastAPI,
    saves it to a temporary file on the local file system,
    and returns the full path to the saved file.

    Args:
        file (UploadFile): The uploaded file to be saved.

    Returns:
        str: The full path of the saved temporary file.
    """
    # create file suffix
    filename = os.path.basename(str(file.filename))
    suffix = f"_{filename}" if filename else f"_{uuid.uuid4()}"

    # Save temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix, mode="wb") as tmp:
        contents = await file.read()
        tmp.write(contents)
        return tmp.name
