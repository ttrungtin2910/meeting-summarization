"""Audio processing service - orchestrates the complete workflow"""

import asyncio
import uuid
from datetime import datetime
from typing import Dict
from uuid import UUID

from fastapi import UploadFile
from loguru import logger

from meeting_summary.api.schemas.audio_processing import (
    MeetingSummaryResponse,
    ProcessingStatusResponse,
    TranscriptionResponse
)
from meeting_summary.domain.exceptions.audio_exceptions import (
    AudioProcessingError,
    UnsupportedFileFormat
)
from meeting_summary.domain.models.audio_task import AudioTask, TaskStatus
from meeting_summary.infrastructure.openai_client.openai_service import OpenAIService
from meeting_summary.infrastructure.storage.file_storage import FileStorage


class AudioProcessingService:
    """Service for handling audio processing workflow"""
    
    def __init__(self, openai_service: OpenAIService, file_storage: FileStorage):
        self.openai_service = openai_service
        self.file_storage = file_storage
        self.tasks: Dict[uuid.UUID, AudioTask] = {}
    
    async def upload_audio(self, file: UploadFile) -> uuid.UUID:
        """Upload audio file and start processing"""
        # Validate file
        self._validate_audio_file(file)
        
        # Read file content immediately to avoid closed file issues
        try:
            file_content = await file.read()
            if not file_content:
                raise ValueError("File is empty or cannot be read")
        except Exception as e:
            raise AudioProcessingError(f"Cannot read uploaded file: {e}")
        
        # Create task
        task = AudioTask(
            filename=file.filename or "unknown",
            file_size=len(file_content),
            file_format=file.filename.split('.')[-1].lower() if file.filename else "unknown"
        )
        
        # Store task BEFORE starting background processing
        self.tasks[task.id] = task
        task.update_status(TaskStatus.UPLOADING, progress=10)
        
        logger.info(f"Created task {task.id} for file {file.filename} ({len(file_content)} bytes)")
        
        # Start background processing with file content
        asyncio.create_task(self._process_audio_background(task.id, file_content, file.filename))
        
        return task.id
    
    async def get_task_status(self, task_id: uuid.UUID) -> ProcessingStatusResponse:
        """Get current status of processing task"""
        if task_id not in self.tasks:
            raise KeyError(f"Task {task_id} not found")
        
        task = self.tasks[task_id]
        
        result = None
        if task.status == TaskStatus.COMPLETED:
            result = {
                "transcription": task.transcription,
                "summary": task.summary_text,
                "key_points": task.key_points,
                "action_items": task.action_items,
                "participants": task.participants
            }
        
        return ProcessingStatusResponse(
            task_id=task.id,
            status=task.status.value,
            progress=task.progress,
            message=task.error_message or f"Task is {task.status.value}",
            result=result,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
    
    async def get_transcription(self, task_id: uuid.UUID) -> TranscriptionResponse:
        """Get transcription result"""
        if task_id not in self.tasks:
            raise KeyError(f"Task {task_id} not found")
        
        task = self.tasks[task_id]
        
        if task.transcription is None:
            raise ValueError("Transcription not ready yet")
        
        return TranscriptionResponse(
            task_id=task.id,
            transcription=task.transcription,
            language=task.transcription_language,
            duration=task.audio_duration,
            confidence=task.transcription_confidence,
            processed_at=task.updated_at
        )
    
    async def get_meeting_summary(self, task_id: uuid.UUID) -> MeetingSummaryResponse:
        """Get meeting summary result"""
        if task_id not in self.tasks:
            raise KeyError(f"Task {task_id} not found")
        
        task = self.tasks[task_id]
        
        if task.summary_text is None:
            raise ValueError("Summary not ready yet")
        
        return MeetingSummaryResponse(
            task_id=task.id,
            summary=task.summary_text,
            key_points=task.key_points or [],
            action_items=task.action_items or [],
            participants=task.participants or [],
            meeting_duration=task.meeting_duration,
            processed_at=task.updated_at
        )
    
    async def process_audio_complete(self, file: UploadFile) -> MeetingSummaryResponse:
        """Complete processing pipeline - synchronous"""
        # Validate file
        self._validate_audio_file(file)
        
        # Create task
        task = AudioTask(
            filename=file.filename,
            file_size=0,
            file_format=file.filename.split('.')[-1].lower()
        )
        
        try:
            # Read file content
            file_content = await file.read()
            if not file_content:
                raise ValueError("File is empty or cannot be read")
            
            # Save file content
            task.update_status(TaskStatus.UPLOADING, progress=20)
            logger.info(f"Saving file for sync processing: {file.filename}")
            file_path = await self.file_storage.save_file_content(file_content, task.id, file.filename)
            task.file_path = file_path
            
            # Transcribe
            task.update_status(TaskStatus.TRANSCRIBING, progress=40)
            logger.info(f"Starting transcription for sync processing")
            transcription_result = await self.openai_service.transcribe_audio(file_path)
            task.set_transcription(
                transcription_result["text"],
                transcription_result.get("language"),
                transcription_result.get("confidence"),
                transcription_result.get("duration")
            )
            
            # Summarize
            task.update_status(TaskStatus.SUMMARIZING, progress=80)
            logger.info(f"Starting summarization for sync processing")
            summary_result = await self.openai_service.summarize_meeting(transcription_result["text"])
            task.set_summary(
                summary_result["summary"],
                summary_result.get("key_points", []),
                summary_result.get("action_items", []),
                summary_result.get("participants", []),
                summary_result.get("meeting_duration")
            )
            
            # Complete
            task.update_status(TaskStatus.COMPLETED)
            
            return MeetingSummaryResponse(
                task_id=task.id,
                summary=task.summary_text,
                key_points=task.key_points or [],
                action_items=task.action_items or [],
                participants=task.participants or [],
                meeting_duration=task.meeting_duration,
                processed_at=task.updated_at,
                audio_file_path=getattr(task, 'persistent_file_path', None),
                transcription=task.transcription,
                transcription_language=task.transcription_language
            )
            
        except Exception as e:
            logger.error(f"Error processing audio: {e}")
            import traceback
            logger.error(f"Full traceback: {traceback.format_exc()}")
            task.update_status(TaskStatus.FAILED, error_message=str(e))
            raise AudioProcessingError(f"Failed to process audio: {e}")
        finally:
            # Move file to persistent storage for inspection instead of deleting
            if hasattr(task, 'file_path') and task.file_path:
                try:
                    persistent_path = await self.file_storage.move_to_persistent_storage(task.file_path, task.id, task.filename)
                    task.persistent_file_path = persistent_path
                    logger.info(f"Audio file saved for inspection: {persistent_path}")
                except Exception as e:
                    logger.warning(f"Failed to move file to persistent storage: {e}")
                    # Fallback to cleanup if move fails
                    await self.file_storage.cleanup_file(task.file_path)
    
    async def _process_audio_background(self, task_id: uuid.UUID, file_content: bytes, filename: str):
        """Background processing of audio file"""
        if task_id not in self.tasks:
            logger.error(f"Task {task_id} not found in tasks dictionary")
            return
            
        task = self.tasks[task_id]
        
        try:
            # Save file content
            task.update_status(TaskStatus.UPLOADING, progress=20)
            logger.info(f"Starting file save for task {task_id}")
            file_path = await self.file_storage.save_file_content(file_content, task_id, filename)
            task.file_path = file_path
            logger.info(f"File saved successfully at {file_path}")
            
            # Transcribe
            task.update_status(TaskStatus.TRANSCRIBING, progress=40)
            logger.info(f"Starting transcription for task {task_id}")
            transcription_result = await self.openai_service.transcribe_audio(file_path)
            task.set_transcription(
                transcription_result["text"],
                transcription_result.get("language"),
                transcription_result.get("confidence"),
                transcription_result.get("duration")
            )
            logger.info(f"Transcription completed for task {task_id}")
            
            # Summarize
            task.update_status(TaskStatus.SUMMARIZING, progress=80)
            logger.info(f"Starting summarization for task {task_id}")
            summary_result = await self.openai_service.summarize_meeting(transcription_result["text"])
            task.set_summary(
                summary_result["summary"],
                summary_result.get("key_points", []),
                summary_result.get("action_items", []),
                summary_result.get("participants", []),
                summary_result.get("meeting_duration")
            )
            logger.info(f"Summarization completed for task {task_id}")
            
            # Complete
            task.update_status(TaskStatus.COMPLETED)
            logger.info(f"Task {task_id} completed successfully")
            
        except Exception as e:
            logger.error(f"Error processing audio {task_id}: {e}")
            import traceback
            logger.error(f"Full traceback: {traceback.format_exc()}")
            task.update_status(TaskStatus.FAILED, error_message=str(e))
        finally:
            # Move file to persistent storage for inspection instead of deleting
            if hasattr(task, 'file_path') and task.file_path:
                try:
                    persistent_path = await self.file_storage.move_to_persistent_storage(task.file_path, task.id, task.filename)
                    task.persistent_file_path = persistent_path
                    logger.info(f"Audio file saved for inspection: {persistent_path}")
                except Exception as e:
                    logger.warning(f"Failed to move file to persistent storage: {e}")
                    # Fallback to cleanup if move fails
                    await self.file_storage.cleanup_file(task.file_path)
    
    async def transcribe_only(self, file: UploadFile) -> TranscriptionResponse:
        """Transcribe audio file without summarization"""
        # Validate file
        self._validate_audio_file(file)
        
        # Read file content
        try:
            file_content = await file.read()
            if not file_content:
                raise ValueError("File is empty or cannot be read")
        except Exception as e:
            raise AudioProcessingError(f"Cannot read uploaded file: {e}")
        
        # Create task
        task = AudioTask(
            filename=file.filename or "unknown",
            file_size=len(file_content),
            file_format=file.filename.split('.')[-1].lower() if file.filename else "unknown"
        )
        
        # Store task
        self.tasks[task.id] = task
        task.update_status(TaskStatus.UPLOADING, progress=20)
        
        try:
            # Save file content
            file_path = await self.file_storage.save_file_content(file_content, task.id, file.filename)
            task.file_path = file_path
            
            # Transcribe only
            task.update_status(TaskStatus.TRANSCRIBING, progress=50)
            logger.info(f"Starting transcription only for task {task.id}")
            transcription_result = await self.openai_service.transcribe_audio(file_path)
            task.set_transcription(
                transcription_result["text"],
                transcription_result.get("language"),
                transcription_result.get("confidence"),
                transcription_result.get("duration")
            )
            
            # Complete transcription
            task.update_status(TaskStatus.COMPLETED, progress=100)
            logger.info(f"Transcription completed for task {task.id}")
            
            return TranscriptionResponse(
                task_id=task.id,
                transcription=task.transcription,
                transcription_language=task.transcription_language,
                audio_duration=task.audio_duration,
                confidence=task.transcription_confidence,
                processed_at=task.updated_at,
                audio_file_path=getattr(task, 'persistent_file_path', None)
            )
            
        except Exception as e:
            logger.error(f"Error transcribing audio: {e}")
            import traceback
            logger.error(f"Full traceback: {traceback.format_exc()}")
            task.update_status(TaskStatus.FAILED, error_message=str(e))
            raise AudioProcessingError(f"Failed to transcribe audio: {e}")
        finally:
            # Move file to persistent storage
            if hasattr(task, 'file_path') and task.file_path:
                try:
                    persistent_path = await self.file_storage.move_to_persistent_storage(task.file_path, task.id, task.filename)
                    task.persistent_file_path = persistent_path
                    logger.info(f"Audio file saved for inspection: {persistent_path}")
                except Exception as e:
                    logger.warning(f"Failed to move file to persistent storage: {e}")
                    await self.file_storage.cleanup_file(task.file_path)

    async def create_summary_from_task(self, task_id: UUID) -> MeetingSummaryResponse:
        """Create meeting summary from existing transcription task"""
        if task_id not in self.tasks:
            raise KeyError(f"Task {task_id} not found")
        
        task = self.tasks[task_id]
        
        if not task.transcription:
            raise ValueError("Task has no transcription to summarize")
        
        try:
            # Update status to summarizing
            task.update_status(TaskStatus.SUMMARIZING, progress=80)
            logger.info(f"Starting summarization for existing task {task_id}")
            
            # Summarize
            summary_result = await self.openai_service.summarize_meeting(task.transcription)
            task.set_summary(
                summary_result["summary"],
                summary_result.get("key_points", []),
                summary_result.get("action_items", []),
                summary_result.get("participants", []),
                summary_result.get("meeting_duration")
            )
            
            # Complete
            task.update_status(TaskStatus.COMPLETED)
            logger.info(f"Summarization completed for task {task_id}")
            
            return MeetingSummaryResponse(
                task_id=task.id,
                summary=task.summary_text,
                key_points=task.key_points or [],
                action_items=task.action_items or [],
                participants=task.participants or [],
                meeting_duration=task.meeting_duration,
                processed_at=task.updated_at,
                audio_file_path=getattr(task, 'persistent_file_path', None),
                transcription=task.transcription,
                transcription_language=task.transcription_language
            )
            
        except Exception as e:
            logger.error(f"Error creating summary for task {task_id}: {e}")
            task.update_status(TaskStatus.FAILED, error_message=str(e))
            raise AudioProcessingError(f"Failed to create summary: {e}")

    def _validate_audio_file(self, file: UploadFile):
        """Validate uploaded audio file"""
        # Check file extension
        if not file.filename:
            raise UnsupportedFileFormat("unknown")
        
        file_ext = file.filename.split('.')[-1].lower()
        supported_formats = {'mp3', 'wav', 'm4a', 'mp4', 'webm', 'flac'}
        
        if file_ext not in supported_formats:
            raise UnsupportedFileFormat(file_ext)
        
        # Note: File size validation would happen during upload in real implementation
