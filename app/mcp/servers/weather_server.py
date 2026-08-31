"""
TripMate AI Standalone Weather MCP Server.
Executed as a subprocess via stdio.
"""

from __future__ import annotations

import os
import sys
from typing import Any

import requests
from mcp.server.fastmcp import FastMCP

REQUEST_TIMEOUT_SECONDS = 20

mcp = FastMCP("Weather MCP Server")


def _get_api_key() -> str:
    api_key = os.environ.get("OPENWEATHER_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("OPENWEATHER_API_KEY environment variable is not set.")
    return api_key


def _request_json(url: str, params: dict[str, Any]) -> dict[str, Any]:
    """Execute OpenWeather HTTP request."""
    try:
        response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        res = getattr(exc, "response", None)
        details = res.text[:500] if res is not None else str(exc)
        raise RuntimeError(f"OpenWeather API request failed: {details}") from exc


@mcp.tool()
def get_current_weather(city: str) -> dict[str, Any]:
    """Get current weather for a city."""
    city = city.strip()
    if not city:
        raise ValueError("City name cannot be empty.")

    api_key = _get_api_key()
    data = _request_json(
        "https://api.openweathermap.org/data/2.5/weather",
        {
            "q": city,
            "appid": api_key,
            "units": "metric",
        },
    )

    return {
        "city": data.get("name", city),
        "temperature_c": data["main"]["temp"],
        "feels_like_c": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "condition": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"],
    }


@mcp.tool()
def get_forecast(city: str) -> dict[str, Any]:
    """Get 5-period 3-hour forecast for a city."""
    city = city.strip()
    if not city:
        raise ValueError("City name cannot be empty.")

    api_key = _get_api_key()
    data = _request_json(
        "https://api.openweathermap.org/data/2.5/forecast",
        {
            "q": city,
            "appid": api_key,
            "units": "metric",
        },
    )

    forecast = [
        {
            "datetime": item["dt_txt"],
            "temperature_c": item["main"]["temp"],
            "condition": item["weather"][0]["description"],
        }
        for item in data.get("list", [])[:5]
    ]

    return {
        "city": data.get("city", {}).get("name", city),
        "forecast": forecast,
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")