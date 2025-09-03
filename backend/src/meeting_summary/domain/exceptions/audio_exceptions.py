"""Exceptions for audio processing domain"""


class AudioProcessingError(Exception):
    """Base exception for audio processing errors"""
    pass


class UnsupportedFileFormat(AudioProcessingError):
    """Exception raised when audio file format is not supported"""
    
    def __init__(self, file_format: str):
        self.file_format = file_format
        super().__init__(f"Unsupported file format: {file_format}. Supported formats: mp3, wav, m4a, mp4, webm, flac")


class FileTooLarge(AudioProcessingError):
    """Exception raised when audio file is too large"""
    
    def __init__(self, file_size: int, max_size: int):
        self.file_size = file_size
        self.max_size = max_size
        super().__init__(f"File size {file_size} bytes exceeds maximum allowed size {max_size} bytes")


class TranscriptionError(AudioProcessingError):
    """Exception raised when audio transcription fails"""
    pass


class SummarizationError(AudioProcessingError):
    """Exception raised when text summarization fails"""
    pass
