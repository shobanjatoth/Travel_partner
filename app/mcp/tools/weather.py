"""
Weather MCP wrapper.
"""

from __future__ import annotations

from app.mcp.registry import get_tool


async def weather_mcp_search(city: str):
    """
    Return current weather.
    """
    tool = await get_tool("weather", "get_current_weather")
    return await tool.ainvoke({"city": city})


async def forecast_mcp_search(city: str):
    """
    Return weather forecast.
    """
    tool = await get_tool("weather", "get_forecast")
    return await tool.ainvoke({"city": city})