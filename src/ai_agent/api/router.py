"""
API Router module.

This module defines and includes all the API routers
"""

from fastapi import APIRouter

from .admin import router as admin_router
from .v1 import router as v1_router

router = APIRouter()
router.include_router(admin_router.router)
router.include_router(v1_router.router)

