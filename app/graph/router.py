
# """
# Routing utilities for the LangGraph workflow.
# """

# from __future__ import annotations

# from app.core.constants import AGENT_ORDER
# from app.graph.state import TravelState

# ROUTE_MAP = {
#     "guardrail_blocked": "guardrail_blocked",
#     "flight_agent": "flight_agent",
#     "hotel_agent": "hotel_agent",
#     "weather_agent": "weather_agent",
#     "budget_agent": "budget_agent",
#     "itinerary_agent": "itinerary_agent",
# }


# def selected_agents(state: TravelState) -> list[str]:
#     """
#     Return selected agents preserving the canonical execution order.
#     """
#     selected = state.get("selected_agents", [])
#     return [agent for agent in AGENT_ORDER if agent in selected]


# def route_from_supervisor(state: TravelState) -> str:
#     """
#     First routing decision: supervisor -> guardrail OR first selected agent.
#     """
#     if not state.get("guardrail_allowed", True):
#         return "guardrail_blocked"

#     agents = selected_agents(state)

#     if not agents:
#         return "itinerary_agent"

#     return agents[0]


# def route_after_agent(current_agent: str):
#     """
#     Factory that creates the routing function used after each specialist agent.
#     flight -> hotel -> weather -> budget -> itinerary
#     """

#     def route(state: TravelState) -> str:
#         agents = selected_agents(state)
#         current_index = AGENT_ORDER.index(current_agent)

#         for next_agent in AGENT_ORDER[current_index + 1 :]:
#             if next_agent in agents:
#                 return next_agent

#         return "itinerary_agent"

#     return route










# """
# Routing utilities for the TripMate LangGraph workflow.
# """

# from __future__ import annotations

# from app.core.constants import AGENT_ORDER
# from app.graph.state import TravelState


# # ---------------------------------------------------------
# # Route Map
# # ---------------------------------------------------------

# ROUTE_MAP = {
#     "guardrail_blocked": "guardrail_blocked",
#     "flight_agent": "flight_agent",
#     "hotel_agent": "hotel_agent",
#     "weather_agent": "weather_agent",
#     "budget_agent": "budget_agent",
#     "itinerary_agent": "itinerary_agent",
# }


# # ---------------------------------------------------------
# # Selected Agents
# # ---------------------------------------------------------

# def selected_agents(
#     state: TravelState,
# ) -> list[str]:
#     """
#     Return selected agents in canonical execution order.
#     """

#     selected = state.get(
#         "selected_agents",
#         [],
#     )

#     return [
#         agent
#         for agent in AGENT_ORDER
#         if agent in selected
#     ]


# # ---------------------------------------------------------
# # Supervisor Router
# # ---------------------------------------------------------

# def route_from_supervisor(
#     state: TravelState,
# ) -> str:
#     """
#     Route from supervisor to either:

#         guardrail_blocked
#               OR
#         first selected specialist agent
#               OR
#         itinerary_agent
#     """

#     # Guardrail rejected request
#     if not state.get(
#         "guardrail_allowed",
#         True,
#     ):
#         return "guardrail_blocked"

#     agents = selected_agents(state)

#     # No specialist agents selected
#     if not agents:
#         return "itinerary_agent"

#     return agents[0]


# # ---------------------------------------------------------
# # Specialist Agent Router
# # ---------------------------------------------------------

# def route_after_agent(
#     current_agent: str,
# ):
#     """
#     Create a router for a specialist agent.

#     Example:

#         flight → hotel → weather → budget → itinerary

#     Agents that were not selected are skipped.
#     """

#     def route(
#         state: TravelState,
#     ) -> str:

#         agents = selected_agents(state)

#         try:
#             current_index = AGENT_ORDER.index(
#                 current_agent
#             )
#         except ValueError:
#             return "itinerary_agent"

#         # Find next selected agent
#         for next_agent in AGENT_ORDER[
#             current_index + 1:
#         ]:
#             if next_agent in agents:
#                 return next_agent

#         # Always finish through itinerary
#         return "itinerary_agent"

#     return route




"""
Routing utilities for the TripMate LangGraph workflow.
"""

from __future__ import annotations

from typing import Callable

from app.core.constants import AGENT_ORDER
from app.graph.state import TravelState


# =========================================================
# Route Map
# =========================================================

ROUTE_MAP: dict[str, str] = {
    "guardrail_blocked": "guardrail_blocked",
    "flight_agent": "flight_agent",
    "hotel_agent": "hotel_agent",
    "weather_agent": "weather_agent",
    "budget_agent": "budget_agent",
    "itinerary_agent": "itinerary_agent",
}


# =========================================================
# Selected Agents
# =========================================================

def selected_agents(state: TravelState) -> list[str]:
    """
    Return the selected specialist agents in the canonical
    execution order defined by AGENT_ORDER.
    """

    selected = state.get("selected_agents") or []

    return [
        agent
        for agent in AGENT_ORDER
        if agent in selected
    ]


# =========================================================
# Supervisor Router
# =========================================================

def route_from_supervisor(state: TravelState) -> str:
    """
    Decide where the workflow should go after the supervisor.

    Flow:

        supervisor
            |
            +--> guardrail_blocked
            |
            +--> first selected specialist agent
            |
            +--> itinerary_agent
    """

    # -----------------------------------------------------
    # Guardrail check
    # -----------------------------------------------------

    if state.get("guardrail_allowed", True) is False:
        return "guardrail_blocked"

    # -----------------------------------------------------
    # Determine selected agents
    # -----------------------------------------------------

    agents = selected_agents(state)

    # -----------------------------------------------------
    # No specialist agents
    # -----------------------------------------------------

    if not agents:
        return "itinerary_agent"

    # -----------------------------------------------------
    # Start with first specialist agent
    # -----------------------------------------------------

    return agents[0]


# =========================================================
# Specialist Agent Router
# =========================================================

def route_after_agent(current_agent: str) -> Callable[[TravelState], str]:
    """
    Return a routing function for a specialist agent.

    Example:

        flight_agent
            ↓
        hotel_agent
            ↓
        weather_agent
            ↓
        budget_agent
            ↓
        itinerary_agent

    Agents not selected by the supervisor are skipped.
    """

    def route(state: TravelState) -> str:
        """
        Determine the next node after the current specialist.
        """

        agents = selected_agents(state)

        # -------------------------------------------------
        # Validate current agent
        # -------------------------------------------------

        if current_agent not in AGENT_ORDER:
            return "itinerary_agent"

        current_index = AGENT_ORDER.index(current_agent)

        # -------------------------------------------------
        # Find next selected specialist
        # -------------------------------------------------

        for next_agent in AGENT_ORDER[current_index + 1:]:
            if next_agent in agents:
                return next_agent

        # -------------------------------------------------
        # All specialists completed
        # -------------------------------------------------

        return "itinerary_agent"

    return route