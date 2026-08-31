"""
LangGraph shared state for TripMate AI.
"""

from __future__ import annotations

import operator
from typing import Annotated, Any, TypedDict

from langchain_core.messages import AnyMessage

from app.core.constants import EMPTY_CONSTRAINTS


class TravelState(TypedDict, total=False):
    # Message log (appends new messages using operator.add)
    messages: Annotated[list[AnyMessage], operator.add]

    user_query: str

    # Supervisor outputs
    guardrail_allowed: bool
    guardrail_reason: str
    selected_agents: list[str]
    trip_constraints: dict[str, Any]
    supervisor_reasoning: str

    # Agent outputs
    flight_results: str
    hotel_results: str
    weather_results: str
    budget_results: str
    itinerary: str

    # Human-in-the-Loop (HITL) review
    approval_request: str
    approved: bool
    human_feedback: str

    # Final output
    final_response: str

    # Performance metrics
    llm_calls: int


def empty_constraints() -> dict[str, Any]:
    """
    Returns a fresh dictionary copy of default trip constraints.
    """
    return EMPTY_CONSTRAINTS.copy()
  