"""
Entry point for running the Meeting Summary FastAPI application.

Initializes the FastAPI app, configures middleware, includes API routers,
and starts the server using Uvicorn.
"""

import sys
from pathlib import Path

import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from meeting_summary.api.router import router
from meeting_summary.config import api_config

app = FastAPI(
    title="Meeting Summary API",
    description="AI-powered meeting summary from audio files using OpenAI Speech-to-Text",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=api_config.allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
