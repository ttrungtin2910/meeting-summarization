"""
Audio processing endpoints.
"""

import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from meeting_summary.api.dependencies.service_dependencies import get_audio_processing_service
from meeting_summary.api.schemas.audio_processing import (
    AudioUploadResponse,
    MeetingSummaryResponse,
    ProcessingStatusResponse,
    TranscriptionResponse
)
from meeting_summary.application.services.audio_processing_service import AudioProcessingService
from meeting_summary.domain.exceptions.audio_exceptions import (
    AudioProcessingError,
    UnsupportedFileFormat
)

router = APIRouter()


@router.post("/upload-audio", response_model=AudioUploadResponse)
async def upload_audio(
    file: UploadFile = File(..., description="Audio file to process"),
    service: AudioProcessingService = Depends(get_audio_processing_service),
):
    """
    Upload an audio file for processing.
    
    Supported formats: mp3, wav, m4a, mp4, webm, flac
    Maximum file size: 25MB
    
    Args:
        file: Audio file to upload and process
        
    Returns:
        AudioUploadResponse: Contains task ID and upload status
        
    Raises:
        400: If file format is unsupported or file is too large
        500: If there's an error processing the file
    """
    try:
        task_id = await service.upload_audio(file)
        return AudioUploadResponse(
            task_id=task_id,
            status="uploaded",
            message="Audio file uploaded successfully. Processing started.",
            uploaded_at=datetime.now()
        )
    except UnsupportedFileFormat as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exception)
        ) from exception
    except AudioProcessingError as exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exception)
        ) from exception


@router.get("/tasks/{task_id}/status", response_model=ProcessingStatusResponse)
async def get_processing_status(
    task_id: uuid.UUID,
    service: AudioProcessingService = Depends(get_audio_processing_service),
):
    """
    Get the status of an audio processing task.
    
    Args:
        task_id: Unique identifier for the processing task
        
    Returns:
        ProcessingStatusResponse: Current status and progress of the task
        
    Raises:
        404: If task ID is not found
    """
    try:
        status_info = await service.get_task_status(task_id)
        return status_info
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found"
        )


@router.get("/tasks/{task_id}/transcription", response_model=TranscriptionResponse)
async def get_transcription(
    task_id: uuid.UUID,
    service: AudioProcessingService = Depends(get_audio_processing_service),
):
    """
    Get the transcription result for a completed task.
    
    Args:
        task_id: Unique identifier for the processing task
        
    Returns:
        TranscriptionResponse: Transcribed text and metadata
        
    Raises:
        404: If task ID is not found
        400: If transcription is not ready yet
    """
    try:
        transcription = await service.get_transcription(task_id)
        return transcription
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found"
        )
    except ValueError as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exception)
        ) from exception


@router.get("/tasks/{task_id}/summary", response_model=MeetingSummaryResponse)
async def get_meeting_summary(
    task_id: uuid.UUID,
    service: AudioProcessingService = Depends(get_audio_processing_service),
):
    """
    Get the meeting summary for a completed task.
    
    Args:
        task_id: Unique identifier for the processing task
        
    Returns:
        MeetingSummaryResponse: Structured meeting summary with key points
        
    Raises:
        404: If task ID is not found
        400: If summary is not ready yet
    """
    try:
        summary = await service.get_meeting_summary(task_id)
        return summary
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found"
        )
    except ValueError as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exception)
        ) from exception


@router.post("/process-audio", response_model=MeetingSummaryResponse)
async def process_audio_complete(
    file: UploadFile = File(..., description="Audio file to process"),
    service: AudioProcessingService = Depends(get_audio_processing_service),
):
    """
    Complete audio processing pipeline - upload, transcribe, and summarize.
    
    This is a synchronous endpoint that processes the entire pipeline.
    For large files, use the async upload + polling approach instead.
    
    Args:
        file: Audio file to process
        
    Returns:
        MeetingSummaryResponse: Complete meeting summary
        
    Raises:
        400: If file format is unsupported or file is too large
        500: If there's an error processing the file
    """
    try:
        summary = await service.process_audio_complete(file)
        return summary
    except UnsupportedFileFormat as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exception)
        ) from exception
    except AudioProcessingError as exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exception)
        ) from exception
