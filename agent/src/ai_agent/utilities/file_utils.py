"""Utility functions for files"""

import os


def delete_file(path: str) -> None:
    """
    Delete file at a path

    Args:
        path: the path of the file to be deleted
    """

    if os.path.exists(path):
        os.remove(path)
