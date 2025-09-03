"""Temporary file handler for uploaded files"""

import asyncio
import os
import tempfile
import uuid
from pathlib import Path
from typing import Optional

import aiofiles
from fastapi import UploadFile
from loguru import logger


class TempFileHandler:
    """Handle temporary files for uploaded content"""
    
    def __init__(self, storage_dir: Optional[str] = None):
        self.storage_dir = storage_dir or tempfile.gettempdir()
        self.storage_path = Path(self.storage_dir)
        self.storage_path.mkdir(exist_ok=True)
        logger.info(f"TempFileHandler initialized with storage: {self.storage_path}")
    
    async def save_upload_file(self, upload_file: UploadFile, task_id: uuid.UUID) -> str:
        """
        Save uploaded file content to temporary file
        
        Args:
            upload_file: FastAPI UploadFile object
            task_id: Unique task identifier
            
        Returns:
            str: Path to saved temporary file
            
        Raises:
            Exception: If file cannot be saved
        """
        try:
            # Generate unique filename
            file_extension = self._get_file_extension(upload_file.filename)
            filename = f"{task_id}.{file_extension}"
            file_path = self.storage_path / filename
            
            logger.info(f"Saving upload file: {upload_file.filename} -> {file_path}")
            
            # Read and save file content
            content = await self._read_upload_content(upload_file)
            await self._write_content_to_file(content, file_path)
            
            # Verify file was created successfully
            if not os.path.exists(file_path):
                raise Exception("File was not created")
                
            file_size = os.path.getsize(file_path)
            if file_size == 0:
                raise Exception("File is empty after saving")
            
            logger.info(f"File saved successfully: {file_path} ({file_size} bytes)")
            return str(file_path)
            
        except Exception as e:
            logger.error(f"Failed to save upload file {upload_file.filename}: {e}")
            raise Exception(f"File save error: {e}")
    
    async def _read_upload_content(self, upload_file: UploadFile) -> bytes:
        """Read content from UploadFile object"""
        try:
            # Method 1: Try reading directly from the file
            content = await upload_file.read()
            
            if content:
                logger.debug(f"Read {len(content)} bytes from upload file")
                return content
            
            # Method 2: If no content, try accessing underlying file
            if hasattr(upload_file, 'file'):
                logger.debug("Trying to read from underlying file object")
                
                # Try different read methods
                if hasattr(upload_file.file, 'read'):
                    if hasattr(upload_file.file, 'seek'):
                        upload_file.file.seek(0)
                    content = upload_file.file.read()
                    
                    if isinstance(content, str):
                        content = content.encode('utf-8')
                    
                    if content:
                        logger.debug(f"Read {len(content)} bytes from underlying file")
                        return content
            
            # Method 3: Try reading in chunks
            logger.debug("Trying chunked read")
            chunks = []
            try:
                while chunk := await upload_file.read(8192):
                    chunks.append(chunk)
                if chunks:
                    content = b''.join(chunks)
                    logger.debug(f"Read {len(content)} bytes in chunks")
                    return content
            except Exception as chunk_error:
                logger.debug(f"Chunked read failed: {chunk_error}")
            
            raise Exception("No content could be read from upload file")
            
        except Exception as e:
            raise Exception(f"Cannot read upload file content: {e}")
    
    async def _write_content_to_file(self, content: bytes, file_path: Path):
        """Write content to file"""
        try:
            async with aiofiles.open(file_path, 'wb') as f:
                await f.write(content)
            logger.debug(f"Wrote {len(content)} bytes to {file_path}")
        except Exception as e:
            raise Exception(f"Cannot write to file {file_path}: {e}")
    
    def _get_file_extension(self, filename: Optional[str]) -> str:
        """Get file extension from filename"""
        if not filename:
            return 'tmp'
        parts = filename.split('.')
        return parts[-1].lower() if len(parts) > 1 else 'tmp'
    
    async def cleanup_file(self, file_path: str):
        """Remove temporary file"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Cleaned up file: {file_path}")
        except Exception as e:
            logger.warning(f"Failed to cleanup file {file_path}: {e}")
    
    async def save_content(self, content: bytes, task_id: uuid.UUID, filename: str) -> str:
        """Save file content directly"""
        try:
            # Generate unique filename
            file_extension = self._get_file_extension(filename)
            file_name = f"{task_id}.{file_extension}"
            file_path = self.storage_path / file_name
            
            logger.info(f"Saving content directly: {filename} -> {file_path}")
            
            # Write content to file
            await self._write_content_to_file(content, file_path)
            
            # Verify file was created successfully
            if not os.path.exists(file_path):
                raise Exception("File was not created")
                
            file_size = os.path.getsize(file_path)
            if file_size == 0:
                raise Exception("File is empty after saving")
            
            logger.info(f"Content saved successfully: {file_path} ({file_size} bytes)")
            return str(file_path)
            
        except Exception as e:
            logger.error(f"Failed to save content for {filename}: {e}")
            raise Exception(f"Content save error: {e}")
    
    async def move_to_persistent(self, temp_path: str, task_id: uuid.UUID, filename: str) -> str:
        """Move file from temp to persistent storage"""
        try:
            # Create persistent storage directory
            persistent_dir = Path("processed_audio_files")
            persistent_dir.mkdir(exist_ok=True)
            
            # Generate persistent filename with timestamp
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_extension = self._get_file_extension(filename)
            persistent_filename = f"{timestamp}_{task_id}_{filename}"
            persistent_path = persistent_dir / persistent_filename
            
            logger.info(f"Moving file: {temp_path} -> {persistent_path}")
            
            # Copy file to persistent location
            import shutil
            shutil.move(temp_path, str(persistent_path))
            
            logger.info(f"File moved successfully to: {persistent_path}")
            return str(persistent_path)
            
        except Exception as e:
            logger.error(f"Failed to move file to persistent storage: {e}")
            raise Exception(f"File move error: {e}")
    
    def get_file_path(self, task_id: uuid.UUID, file_extension: str) -> str:
        """Get file path for task"""
        filename = f"{task_id}.{file_extension}"
        return str(self.storage_path / filename)
