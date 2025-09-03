"""Service dependencies for dependency injection"""

from fastapi import Depends

from meeting_summary.application.services.audio_processing_service import AudioProcessingService
from meeting_summary.infrastructure.openai_client.openai_service import OpenAIService
from meeting_summary.infrastructure.storage.file_storage import FileStorage

# Global singletons to maintain state across requests
_openai_service: OpenAIService = None
_file_storage: FileStorage = None 
_audio_processing_service: AudioProcessingService = None


def get_openai_service() -> OpenAIService:
    """Get OpenAI service instance (singleton)"""
    global _openai_service
    if _openai_service is None:
        _openai_service = OpenAIService()
    return _openai_service


def get_file_storage() -> FileStorage:
    """Get file storage instance (singleton)"""
    global _file_storage
    if _file_storage is None:
        _file_storage = FileStorage()
    return _file_storage


def get_audio_processing_service(
    openai_service: OpenAIService = Depends(get_openai_service),
    file_storage: FileStorage = Depends(get_file_storage),
) -> AudioProcessingService:
    """Get audio processing service instance (singleton)"""
    global _audio_processing_service
    if _audio_processing_service is None:
        _audio_processing_service = AudioProcessingService(openai_service, file_storage)
    return _audio_processing_service
