"""
API Router module for version 1.

This module defines and includes all the API routers for the version 1,
grouping them with different tags.
"""

from fastapi import APIRouter

from . import audio_processing

router = APIRouter(prefix="/v1")
router.include_router(audio_processing.router, tags=["audio-processing"])
