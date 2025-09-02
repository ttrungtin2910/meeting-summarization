"""
API Router module.

This module defines and includes all the API routers for the version 1,
grouping them with different tags.
"""

from fastapi import APIRouter

from . import (app_clients, auth, categories, chat, chat_sessions, collections,
               documents, external_users, sync)

router = APIRouter(prefix="/v1")
router.include_router(chat.router, tags=["chat"])
router.include_router(documents.router, tags=["documents"])
router.include_router(categories.router, tags=["categories"])
router.include_router(collections.router, tags=["collections"])
router.include_router(sync.router, tags=["sync"])
router.include_router(chat_sessions.router, tags=["chat-sessions"])
router.include_router(auth.router, tags=["auth"])
router.include_router(external_users.router, tags=["external-users"])
router.include_router(app_clients.router, tags=["app-clients"])
