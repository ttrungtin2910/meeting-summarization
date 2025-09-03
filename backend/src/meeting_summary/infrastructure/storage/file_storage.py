"""File storage service for handling uploaded audio files"""

import os
import tempfile
import uuid
from pathlib import Path
from typing import Optional

from fastapi import UploadFile
from loguru import logger

from .temp_file_handler import TempFileHandler


class FileStorage:
    """Service for handling file storage operations"""
    
    def __init__(self, storage_dir: Optional[str] = None):
        self.temp_handler = TempFileHandler(storage_dir)
    
    async def save_file(self, file: UploadFile, task_id: uuid.UUID) -> str:
        """Save uploaded file to storage"""
        try:
            logger.info(f"Saving file: {file.filename} for task {task_id}")
            return await self.temp_handler.save_upload_file(file, task_id)
        except Exception as e:
            logger.error(f"FileStorage save_file error: {e}")
            raise Exception(f"File storage error: {e}")
    
    async def save_file_content(self, content: bytes, task_id: uuid.UUID, filename: str) -> str:
        """Save file content directly to storage"""
        try:
            logger.info(f"Saving file content: {filename} for task {task_id} ({len(content)} bytes)")
            return await self.temp_handler.save_content(content, task_id, filename)
        except Exception as e:
            logger.error(f"FileStorage save_file_content error: {e}")
            raise Exception(f"File storage error: {e}")
    
    async def cleanup_file(self, file_path: str):
        """Remove temporary file"""
        await self.temp_handler.cleanup_file(file_path)
    
    async def move_to_persistent_storage(self, temp_path: str, task_id: uuid.UUID, filename: str) -> str:
        """Move file from temp to persistent storage for inspection"""
        try:
            logger.info(f"Moving file to persistent storage: {filename} for task {task_id}")
            return await self.temp_handler.move_to_persistent(temp_path, task_id, filename)
        except Exception as e:
            logger.error(f"FileStorage move_to_persistent_storage error: {e}")
            raise Exception(f"File move error: {e}")
    
    def get_file_path(self, task_id: uuid.UUID, file_extension: str) -> str:
        """Get file path for task"""
        return self.temp_handler.get_file_path(task_id, file_extension)
