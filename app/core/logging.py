"""
Centralized logging configuration for TripMate AI.
"""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from app.core.config import settings

LOG_FORMAT = (
    "%(asctime)s | %(levelname)-8s | "
    "%(name)s | %(filename)s:%(lineno)d | %(message)s"
)


def setup_logging() -> None:
    """
    Configure application-wide logging.
    This function should be called only once during application startup.
    """
    log_path = Path(settings.LOG_FILE)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(LOG_FORMAT)

    file_handler = RotatingFileHandler(
        filename=log_path,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
        handlers=[
            console_handler,
            file_handler,
        ],
        force=True,
    )


def get_logger(name: str) -> logging.Logger:
    """
    Return a configured logger.
    """
    return logging.getLogger(name)