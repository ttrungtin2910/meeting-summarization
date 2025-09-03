"""
API Router module.

This module defines and includes all the API routers
"""

from fastapi import APIRouter

from .v1 import router as v1_router
from .v1.transcription import router as transcription_router

router = APIRouter()
router.include_router(v1_router.router)
router.include_router(transcription_router, prefix="/v1")
# Add direct transcription route for backward compatibility
router.include_router(transcription_router)
