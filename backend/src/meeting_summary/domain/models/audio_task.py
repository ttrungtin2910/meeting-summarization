"""Audio processing task domain model"""

from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    """Status of audio processing task"""
    PENDING = "pending"
    UPLOADING = "uploading"
    TRANSCRIBING = "transcribing"
    SUMMARIZING = "summarizing"
    COMPLETED = "completed"
    FAILED = "failed"


class AudioTask(BaseModel):
    """Domain model for audio processing task"""
    
    id: UUID = Field(default_factory=uuid4)
    filename: str
    file_path: Optional[str] = None
    persistent_file_path: Optional[str] = None  # Path to saved file for inspection
    file_size: int
    file_format: str
    status: TaskStatus = TaskStatus.PENDING
    progress: int = 0
    error_message: Optional[str] = None
    
    # Processing results
    transcription: Optional[str] = None
    transcription_language: Optional[str] = None
    transcription_confidence: Optional[float] = None
    audio_duration: Optional[float] = None
    
    # Summary results
    summary_text: Optional[str] = None
    key_points: Optional[List[str]] = None
    action_items: Optional[List[str]] = None
    participants: Optional[List[str]] = None
    meeting_duration: Optional[str] = None
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    
    def update_status(self, status: TaskStatus, progress: int = None, error_message: str = None):
        """Update task status and metadata"""
        self.status = status
        self.updated_at = datetime.now()
        
        if progress is not None:
            self.progress = progress
            
        if error_message is not None:
            self.error_message = error_message
            
        if status == TaskStatus.COMPLETED:
            self.completed_at = datetime.now()
            self.progress = 100
    
    def set_transcription(self, transcription: str, language: str = None, confidence: float = None, duration: float = None):
        """Set transcription results"""
        self.transcription = transcription
        self.transcription_language = language
        self.transcription_confidence = confidence
        self.audio_duration = duration
        self.updated_at = datetime.now()
    
    def set_summary(self, summary: str, key_points: List[str] = None, action_items: List[str] = None, 
                   participants: List[str] = None, meeting_duration: str = None):
        """Set summary results"""
        self.summary_text = summary
        self.key_points = key_points or []
        self.action_items = action_items or []
        self.participants = participants or []
        self.meeting_duration = meeting_duration
        self.updated_at = datetime.now()
