"""
Custom exceptions used across TripMate AI.
"""

from __future__ import annotations


class TripMateException(Exception):
    """Base application exception."""

    pass


class ConfigurationError(TripMateException):
    """Raised when configuration is invalid."""

    pass


class MCPServerError(TripMateException):
    """Raised when an MCP server fails."""

    pass


class WeatherServiceError(MCPServerError):
    """Weather MCP failure."""

    pass


class AviationServiceError(MCPServerError):
    """Aviation MCP failure."""

    pass


class TavilyServiceError(MCPServerError):
    """Tavily MCP failure."""

    pass


class DestinationExtractionError(TripMateException):
    """Raised when destination extraction fails."""

    pass


class InvalidTravelRequest(TripMateException):
    """Raised when the guardrail blocks a request."""

    pass


class LLMResponseError(TripMateException):
    """Raised when an LLM response cannot be parsed."""

    pass


class DatabaseConnectionError(TripMateException):
    """Raised when PostgreSQL connection fails."""

    pass


class GraphExecutionError(TripMateException):
    """Raised when LangGraph execution fails."""

    pass