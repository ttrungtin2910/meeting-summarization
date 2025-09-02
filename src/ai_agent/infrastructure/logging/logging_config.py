"""
This module configures and utilizes the loguru library for application logging.

Features:
- Logs to file with detailed formatting.
- Automatically rotates log files

Usage:
- from core.infrastructure.logging import logger
"""


import sys
from pathlib import Path

from loguru import logger

Path("logs").mkdir(parents=True, exist_ok=True)

logger.remove()

logger.add(
    sys.stdout,
    level="DEBUG",
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss!UTC}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{file}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )
)

logger.add(
    "logs/{time}.log",
    level="DEBUG",
    rotation="25 MB",
    retention="30 days",
    compression="zip",
    format=(
        "{time:YYYY-MM-DD HH:mm:ss!UTC} | "
        "{level: <8} | "
        "{file}:{function}:{line} - "
        "{message}"
    )
)
