"""
Centralized MultiServer MCP Client.
"""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path
from typing import Optional

import certifi
from langchain_mcp_adapters.client import MultiServerMCPClient

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

# SSL Certificates setup
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

BASE_DIR = Path(__file__).resolve().parents[2]

WEATHER_SERVER_PATH = (
    BASE_DIR
    / "app"
    / "mcp"
    / "servers"
    / "weather_server.py"
)

UVX_COMMAND = shutil.which("uvx") or "uvx"


def subprocess_env(**updates: str | None) -> dict[str, str]:
    """
    Preserve current environment while injecting
    API keys for subprocess MCP servers.
    """
    env = os.environ.copy()
    for key, value in updates.items():
        if value:
            env[key] = value
    return env


_client_instance: Optional[MultiServerMCPClient] = None


def get_mcp_client() -> MultiServerMCPClient:
    """
    Lazy initialization of MultiServerMCPClient to prevent eager startup crashes.
    """
    global _client_instance
    if _client_instance is None:
        _client_instance = MultiServerMCPClient(
            {
                "tavily": {
                    "transport": "streamable_http",
                    "url": (
                        "https://mcp.tavily.com/mcp/"
                        f"?tavilyApiKey={settings.TAVILY_API_KEY}"
                    ),
                },
                "aviationstack": {
                    "transport": "stdio",
                    "command": UVX_COMMAND,
                    "args": ["aviationstack-mcp"],
                    "env": subprocess_env(
                        AVIATION_STACK_API_KEY=settings.AVIATION_STACK_API_KEY,
                    ),
                },
                "weather": {
                    "transport": "stdio",
                    "command": sys.executable,
                    "args": [str(WEATHER_SERVER_PATH)],
                    "env": subprocess_env(
                        OPENWEATHER_API_KEY=settings.OPENWEATHER_API_KEY,
                    ),
                },
            }
        )
        logger.info("MultiServer MCP Client initialized.")
    return _client_instance