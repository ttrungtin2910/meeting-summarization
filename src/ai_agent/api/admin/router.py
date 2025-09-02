"""
API Router module.

This module defines and includes all the API routers for the admin,
grouping them with different tags.
"""

from fastapi import APIRouter

from . import organizations

router = APIRouter(prefix="/admin")
router.include_router(organizations.router, tags=["organizations"])
