"""
Base interface for storage services.

Defines abstract methods for uploading, downloading, delete
and listing files in a remote storage system.
"""


from abc import ABC, abstractmethod


class BaseStorage(ABC):
    """
    Interface for a generic storage service.
    """
    @abstractmethod
    def upload(self, local_path: str, remote_path: str):
        """
        Upload a local file to the remote storage.

        Args:
            local_path (str): Path to the local file.
            remote_path (str): Path where the file will be stored in remote storage.
        """

    @abstractmethod
    def download(self, remote_path: str, local_path: str):
        """
        Download a file from the remote storage to local disk.

        Args:
            remote_path (str): Path to the file in remote storage.
            local_path (str): Path where the file will be saved locally.
        """

    @abstractmethod
    def list_files(self, prefix: str = "") -> list:
        """
        List all files in remote storage under a given prefix (folder-like).

        Args:
            prefix (str, optional): The prefix to filter files. Defaults to "".

        Returns:
            list: List of file names.
        """

    @abstractmethod
    def delete(self, remote_path: str):
        """
        Delete a file from the remote storage.

        Args:
            remote_path (str): Path to the file in remote storage.
        """

    @abstractmethod
    def generate_download_url(self, remote_path: str) -> str:
        """
        Generate a temporary downloadable URL

        Args:
            remote_path (str): Path to the file in remote storage.

        Returns:
            str:  A temporary downloadable URL for the file at the given remote path.
        """
