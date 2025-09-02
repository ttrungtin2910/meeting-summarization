"""
Entry point for running the FastAPI application.

Initializes the FastAPI app, configures middleware, includes API routers,
and starts the server using Uvicorn.
"""

import sys
from pathlib import Path

import uvicorn
from dotenv import load_dotenv

# pylint: disable=wrong-import-position
# Load environment variables
load_dotenv(override=True)
sys.path.insert(0, str(Path(__file__).resolve().parent/ "src"))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ai_agent.api.router import router
from ai_agent.config import APIConfig

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = APIConfig.allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
