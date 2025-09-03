"""Meeting summary domain model"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class MeetingSummary(BaseModel):
    """Domain model for meeting summary"""
    
    task_id: UUID
    summary: str
    key_points: List[str] = Field(default_factory=list)
    action_items: List[str] = Field(default_factory=list)
    participants: List[str] = Field(default_factory=list)
    meeting_duration: Optional[str] = None
    
    # Metadata
    original_transcription: str
    audio_duration: Optional[float] = None
    transcription_language: Optional[str] = None
    transcription_confidence: Optional[float] = None
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.now)
    
    @classmethod
    def from_transcription(cls, task_id: UUID, transcription: str, summary_data: dict) -> "MeetingSummary":
        """Create meeting summary from transcription and summary data"""
        return cls(
            task_id=task_id,
            summary=summary_data.get("summary", ""),
            key_points=summary_data.get("key_points", []),
            action_items=summary_data.get("action_items", []),
            participants=summary_data.get("participants", []),
            meeting_duration=summary_data.get("meeting_duration"),
            original_transcription=transcription
        )
