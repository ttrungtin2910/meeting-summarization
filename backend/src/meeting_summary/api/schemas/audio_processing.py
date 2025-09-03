"""Schemas for audio processing endpoints"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class AudioUploadResponse(BaseModel):
    """Response for audio upload"""
    task_id: UUID
    status: str
    message: str
    uploaded_at: datetime


class TranscriptionResponse(BaseModel):
    """Response for audio transcription"""
    task_id: UUID
    transcription: str
    language: Optional[str] = None
    duration: Optional[float] = None
    confidence: Optional[float] = None
    processed_at: datetime


class TranscriptionResponse(BaseModel):
    """Response for transcription only"""
    task_id: UUID
    transcription: str
    transcription_language: Optional[str] = None
    audio_duration: Optional[float] = None
    confidence: Optional[float] = None
    processed_at: datetime
    audio_file_path: Optional[str] = None

class MeetingSummaryResponse(BaseModel):
    """Response for meeting summary"""
    task_id: UUID
    summary: str
    key_points: List[str]
    action_items: List[str]
    participants: List[str]
    meeting_duration: Optional[str] = None
    processed_at: datetime
    audio_file_path: Optional[str] = None  # Path to saved audio file for inspection
    transcription: Optional[str] = None  # Original transcription text
    transcription_language: Optional[str] = None  # Detected language


class ProcessingStatusResponse(BaseModel):
    """Response for processing status"""
    task_id: UUID
    status: str  # "pending", "processing", "completed", "failed"
    progress: int  # 0-100
    message: str
    result: Optional[dict] = None
    created_at: datetime
    updated_at: datetime
