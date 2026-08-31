"""
Shared MCP tool loader.
"""

from __future__ import annotations

import shutil

from app.core.config import settings
from app.core.exceptions import MCPServerError
from app.core.logging import get_logger
from app.mcp.client import WEATHER_SERVER_PATH, get_mcp_client

logger = get_logger(__name__)


def _require(value: str | None, name: str) -> str:
    """Validate required environment variables."""
    if not value:
        raise MCPServerError(f"{name} is missing.")
    return value


async def get_tool(server_name: str, tool_name: str):
    """
    Return one MCP tool.
    Only the requested server is loaded.
    """
    if server_name == "tavily":
        _require(settings.TAVILY_API_KEY, "TAVILY_API_KEY")

    elif server_name == "aviationstack":
        _require(settings.AVIATION_STACK_API_KEY, "AVIATION_STACK_API_KEY")
        if shutil.which("uvx") is None:
            raise MCPServerError("uvx is not installed on this host.")

    elif server_name == "weather":
        _require(settings.OPENWEATHER_API_KEY, "OPENWEATHER_API_KEY")
        if not WEATHER_SERVER_PATH.exists():
            raise FileNotFoundError(f"Weather server script missing at {WEATHER_SERVER_PATH}")

    logger.info("Loading MCP tool '%s' from server '%s'", tool_name, server_name)
    client = get_mcp_client()
    tools = await client.get_tools(server_name=server_name)

    for tool in tools:
        if tool.name == tool_name:
            return tool

    available = ", ".join(tool.name for tool in tools)
    raise MCPServerError(f"Tool '{tool_name}' not found. Available tools: {available}")