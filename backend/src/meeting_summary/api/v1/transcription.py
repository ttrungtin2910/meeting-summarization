"""Transcription-only API endpoints"""

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from uuid import UUID

from meeting_summary.api.dependencies.service_dependencies import get_audio_processing_service
from meeting_summary.api.schemas.audio_processing import TranscriptionResponse
from meeting_summary.application.services.audio_processing_service import AudioProcessingService
from meeting_summary.domain.exceptions.audio_exceptions import AudioProcessingError

router = APIRouter(prefix="/transcription", tags=["transcription"])


@router.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio_only(
    file: UploadFile = File(..., description="Audio file to transcribe"),
    service: AudioProcessingService = Depends(get_audio_processing_service),
):
    """
    Transcribe audio file only (no summarization)
    """
    try:
        # Process only transcription
        result = await service.transcribe_only(file)
        return result
    except AudioProcessingError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/summarize/{task_id}")
async def create_summary_from_transcription(
    task_id: UUID,
    service: AudioProcessingService = Depends(get_audio_processing_service),
):
    """
    Create meeting summary from existing transcription
    """
    try:
        result = await service.create_summary_from_task(task_id)
        return result
    except KeyError:
        raise HTTPException(status_code=404, detail="Task not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
