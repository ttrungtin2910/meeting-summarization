"""
Azure Blob Storage service implementation.

Provides a concrete implementation of BaseStorageService
using Azure Blob Storage.
"""

from datetime import datetime, timedelta, timezone

from azure.storage.blob import (BlobSasPermissions, BlobServiceClient,
                                generate_blob_sas)

from .base import BaseStorage


class AzureBlobStorage(BaseStorage):
    """
    Implementation of IStorageService using Azure Blob Storage.
    """

    def __init__(self, config):
        """
        Initializes the Azure Blob Storage client using connection string and container.
        """
        self.account_name = config.account_name
        self.account_key = config.account_key
        self.expire_minutes = config.expire_minutes
        self.container_name = config.container_name

        connection_string = (
            f"DefaultEndpointsProtocol=https;"
            f"AccountName={self.account_name};"
            f"AccountKey={self.account_key};"
            f"EndpointSuffix=core.windows.net"
        )
        self.client = BlobServiceClient.from_connection_string(
            connection_string
        )
        self.container = self.client.get_container_client(self.container_name)

    def upload(self, local_path: str, remote_path: str):
        """
        Upload a local file to Azure Blob Storage and return its URI.

        Args:
            local_path (str): Path to local file.
            remote_path (str): Path to store in blob container (e.g. "documents/myfile.pdf").
        """
        with open(local_path, "rb") as f:
            self.container.upload_blob(name=remote_path, data=f, overwrite=True)

    def download(self, remote_path: str, local_path: str):
        """
        Download a file from Azure Blob Storage to local disk.
        """
        blob = self.container.download_blob(remote_path)
        with open(local_path, "wb") as f:
            f.write(blob.readall())

    def list_files(self, prefix: str = "") -> list:
        """
        List all blobs in the container with optional prefix.
        """
        return [b.name for b in self.container.list_blobs(name_starts_with=prefix)]

    def delete(self, remote_path: str):
        """
        Delete a blob from the container.
        """
        self.container.delete_blob(remote_path)

    def generate_download_url(self, remote_path: str) -> str:
        """
        Generate a temporary downloadable URL

        Args:
            remote_path (str): Path to the file in remote storage.

        Returns:
            str:  A temporary downloadable URL for the file at the given remote path.
        """
        expire_time = datetime.now(tz=timezone.utc) + timedelta(minutes=self.expire_minutes)
        sas_token = generate_blob_sas(
            account_name = self.account_name,
            account_key=self.account_key,
            container_name = self.container_name,
            blob_name=remote_path,
            permission=BlobSasPermissions(read=True),
            expiry=expire_time,
        )

        blob_url = f"https://{self.account_name}.blob.core.windows.net/\
{self.container_name}/{remote_path}"

        return f"{blob_url}?{sas_token}"
