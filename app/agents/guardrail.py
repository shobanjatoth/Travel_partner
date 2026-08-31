"""
Travel Input Guardrail Node
"""

from __future__ import annotations

from langchain_core.messages import AIMessage

from app.core.logging import get_logger
from app.graph.state import TravelState

logger = get_logger(__name__)


def guardrail_blocked_agent(state: TravelState) -> TravelState:
    """
    Handles blocked requests.
    Executed only when the supervisor determines that the request is outside scope.
    """
    reason = (
        state.get("final_response")
        or state.get("guardrail_reason")
        or "TripMate AI can only assist with travel planning requests."
    )

    logger.warning("Guardrail blocked request: %s", reason)

    return {
        "final_response": reason,
        "messages": [AIMessage(content=reason)],
    }