"""
Application-wide constants.
"""

from __future__ import annotations

# HTTP
REQUEST_TIMEOUT_SECONDS = 20

# MCP
WEATHER_SERVER_NAME = "weather"
TAVILY_SERVER_NAME = "tavily"
AVIATION_SERVER_NAME = "aviationstack"

# Agent Names
FLIGHT_AGENT = "flight_agent"
HOTEL_AGENT = "hotel_agent"
WEATHER_AGENT = "weather_agent"
BUDGET_AGENT = "budget_agent"
ITINERARY_AGENT = "itinerary_agent"
GUARDRAIL_AGENT = "guardrail_blocked"

KNOWN_AGENTS = {
    FLIGHT_AGENT,
    HOTEL_AGENT,
    WEATHER_AGENT,
    BUDGET_AGENT,
    ITINERARY_AGENT,
}

AGENT_ORDER = [
    FLIGHT_AGENT,
    HOTEL_AGENT,
    WEATHER_AGENT,
    BUDGET_AGENT,
    ITINERARY_AGENT,
]

# LLM
MAX_JSON_RETRY = 2

# API
API_PREFIX = "/api"
HEALTH_ROUTE = "/health"

# Conversation
DEFAULT_THREAD_PREFIX = "user_"

# Messages
EMPTY_DESTINATION_ERROR = "The destination could not be extracted."
EMPTY_CITY_ERROR = "City cannot be empty."

# Default Constraints Structure
EMPTY_CONSTRAINTS = {
    "budget": None,
    "destination": None,
    "duration": None,
    "dates": None,
    "interests": [],
}