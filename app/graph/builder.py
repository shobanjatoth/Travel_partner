# """
# LangGraph Workflow Builder for TripMate AI.
# """

# from __future__ import annotations

# from langgraph.graph import END, START, StateGraph

# from app.agents.budget import budget_agent
# from app.agents.flight import flight_agent
# from app.agents.guardrail import guardrail_blocked_agent
# from app.agents.hotel import hotel_agent
# from app.agents.itinerary import itinerary_agent
# from app.agents.responder import responder_agent
# from app.agents.reviewer import reviewer_agent
# from app.agents.supervisor import supervisor_agent
# from app.agents.weather import weather_agent
# from app.database.checkpoint import checkpointer
# from app.graph.router import ROUTE_MAP, route_after_agent, route_from_supervisor
# from app.graph.state import TravelState

# # Instantiate graph
# graph = StateGraph(TravelState)

# # Add Nodes
# graph.add_node("supervisor", supervisor_agent)
# graph.add_node("guardrail_blocked", guardrail_blocked_agent)
# graph.add_node("flight_agent", flight_agent)
# graph.add_node("hotel_agent", hotel_agent)
# graph.add_node("weather_agent", weather_agent)
# graph.add_node("budget_agent", budget_agent)
# graph.add_node("itinerary_agent", itinerary_agent)
# graph.add_node("human_approval", reviewer_agent)
# graph.add_node("final_agent", responder_agent)

# # Add Initial Entry
# graph.add_edge(START, "supervisor")

# # Conditional Router Edges
# graph.add_conditional_edges(
#     "supervisor",
#     route_from_supervisor,
#     ROUTE_MAP,
# )

# graph.add_conditional_edges(
#     "flight_agent",
#     route_after_agent("flight_agent"),
#     ROUTE_MAP,
# )

# graph.add_conditional_edges(
#     "hotel_agent",
#     route_after_agent("hotel_agent"),
#     ROUTE_MAP,
# )

# graph.add_conditional_edges(
#     "weather_agent",
#     route_after_agent("weather_agent"),
#     ROUTE_MAP,
# )

# graph.add_conditional_edges(
#     "budget_agent",
#     route_after_agent("budget_agent"),
#     ROUTE_MAP,
# )

# # Terminal Pipelines
# graph.add_edge("itinerary_agent", "human_approval")
# graph.add_edge("human_approval", "final_agent")
# graph.add_edge("final_agent", END)
# graph.add_edge("guardrail_blocked", END)

# # Compile Graph with Checkpointer
# travel_graph = graph.compile(checkpointer=checkpointer)







# """
# LangGraph Workflow Builder for TripMate AI.
# """

# from __future__ import annotations

# from langgraph.graph import END, START, StateGraph

# from app.agents.budget import budget_agent
# from app.agents.flight import flight_agent
# from app.agents.guardrail import guardrail_blocked_agent
# from app.agents.hotel import hotel_agent
# from app.agents.itinerary import itinerary_agent
# from app.agents.responder import responder_agent
# from app.agents.reviewer import reviewer_agent
# from app.agents.supervisor import supervisor_agent
# from app.agents.weather import weather_agent

# from app.database.checkpoint import checkpointer

# from app.graph.router import (
#     ROUTE_MAP,
#     route_after_agent,
#     route_from_supervisor,
# )

# from app.graph.state import TravelState


# # ---------------------------------------------------------
# # Create Graph
# # ---------------------------------------------------------

# graph = StateGraph(TravelState)


# # ---------------------------------------------------------
# # Add Nodes
# # ---------------------------------------------------------

# graph.add_node(
#     "supervisor",
#     supervisor_agent,
# )

# graph.add_node(
#     "guardrail_blocked",
#     guardrail_blocked_agent,
# )

# graph.add_node(
#     "flight_agent",
#     flight_agent,
# )

# graph.add_node(
#     "hotel_agent",
#     hotel_agent,
# )

# graph.add_node(
#     "weather_agent",
#     weather_agent,
# )

# graph.add_node(
#     "budget_agent",
#     budget_agent,
# )

# graph.add_node(
#     "itinerary_agent",
#     itinerary_agent,
# )

# graph.add_node(
#     "human_approval",
#     reviewer_agent,
# )

# graph.add_node(
#     "final_agent",
#     responder_agent,
# )


# # ---------------------------------------------------------
# # Entry Point
# # ---------------------------------------------------------

# graph.add_edge(
#     START,
#     "supervisor",
# )


# # ---------------------------------------------------------
# # Supervisor Routing
# # ---------------------------------------------------------

# graph.add_conditional_edges(
#     "supervisor",
#     route_from_supervisor,
#     ROUTE_MAP,
# )


# # ---------------------------------------------------------
# # Specialist Agent Routing
# # ---------------------------------------------------------

# graph.add_conditional_edges(
#     "flight_agent",
#     route_after_agent("flight_agent"),
#     ROUTE_MAP,
# )

# graph.add_conditional_edges(
#     "hotel_agent",
#     route_after_agent("hotel_agent"),
#     ROUTE_MAP,
# )

# graph.add_conditional_edges(
#     "weather_agent",
#     route_after_agent("weather_agent"),
#     ROUTE_MAP,
# )

# graph.add_conditional_edges(
#     "budget_agent",
#     route_after_agent("budget_agent"),
#     ROUTE_MAP,
# )


# # ---------------------------------------------------------
# # Itinerary → Human Approval → Final Response
# # ---------------------------------------------------------

# graph.add_edge(
#     "itinerary_agent",
#     "human_approval",
# )

# graph.add_edge(
#     "human_approval",
#     "final_agent",
# )

# graph.add_edge(
#     "final_agent",
#     END,
# )


# # ---------------------------------------------------------
# # Guardrail Block
# # ---------------------------------------------------------

# graph.add_edge(
#     "guardrail_blocked",
#     END,
# )


# # ---------------------------------------------------------
# # Compile Graph
# # ---------------------------------------------------------

# travel_graph = graph.compile(
#     checkpointer=checkpointer,
# )











# """
# LangGraph Workflow Builder for TripMate AI.
# """

# from __future__ import annotations

# from langgraph.graph import END, START, StateGraph

# from app.agents.budget import budget_agent
# from app.agents.flight import flight_agent
# from app.agents.guardrail import guardrail_blocked_agent
# from app.agents.hotel import hotel_agent
# from app.agents.itinerary import itinerary_agent
# from app.agents.responder import responder_agent
# from app.agents.reviewer import reviewer_agent
# from app.agents.supervisor import supervisor_agent
# from app.agents.weather import weather_agent

# from app.database.checkpoint import checkpointer

# from app.graph.router import (
#     ROUTE_MAP,
#     route_after_agent,
#     route_from_supervisor,
# )

# from app.graph.state import TravelState


# # =========================================================
# # Create Graph
# # =========================================================

# graph = StateGraph(TravelState)


# # =========================================================
# # Nodes
# # =========================================================

# graph.add_node("supervisor", supervisor_agent)
# graph.add_node("guardrail_blocked", guardrail_blocked_agent)

# graph.add_node("flight_agent", flight_agent)
# graph.add_node("hotel_agent", hotel_agent)
# graph.add_node("weather_agent", weather_agent)
# graph.add_node("budget_agent", budget_agent)

# graph.add_node("itinerary_agent", itinerary_agent)
# graph.add_node("human_approval", reviewer_agent)
# graph.add_node("final_agent", responder_agent)


# # =========================================================
# # Entry
# # =========================================================

# graph.add_edge(
#     START,
#     "supervisor",
# )


# # =========================================================
# # Supervisor Routing
# # =========================================================

# graph.add_conditional_edges(
#     "supervisor",
#     route_from_supervisor,
#     ROUTE_MAP,
# )


# # =========================================================
# # Agent Routing
# # =========================================================

# graph.add_conditional_edges(
#     "flight_agent",
#     route_after_agent("flight_agent"),
#     ROUTE_MAP,
# )

# graph.add_conditional_edges(
#     "hotel_agent",
#     route_after_agent("hotel_agent"),
#     ROUTE_MAP,
# )

# graph.add_conditional_edges(
#     "weather_agent",
#     route_after_agent("weather_agent"),
#     ROUTE_MAP,
# )

# graph.add_conditional_edges(
#     "budget_agent",
#     route_after_agent("budget_agent"),
#     ROUTE_MAP,
# )


# # =========================================================
# # Final Pipeline
# # =========================================================

# graph.add_edge(
#     "itinerary_agent",
#     "human_approval",
# )

# graph.add_edge(
#     "human_approval",
#     "final_agent",
# )

# graph.add_edge(
#     "final_agent",
#     END,
# )


# # =========================================================
# # Guardrail
# # =========================================================

# graph.add_edge(
#     "guardrail_blocked",
#     END,
# )


# # =========================================================
# # Compile
# # =========================================================

# travel_graph = graph.compile(
#     checkpointer=checkpointer,
# )










# """
# LangGraph Workflow Builder for TripMate AI.

# Database-free version:
# - No PostgreSQL
# - No SQLite
# - No LangGraph checkpointer
# - No persistent memory
# """

# from __future__ import annotations

# from langgraph.graph import END, START, StateGraph

# from app.agents.budget import budget_agent
# from app.agents.flight import flight_agent
# from app.agents.guardrail import guardrail_blocked_agent
# from app.agents.hotel import hotel_agent
# from app.agents.itinerary import itinerary_agent
# from app.agents.responder import responder_agent
# from app.agents.reviewer import reviewer_agent
# from app.agents.supervisor import supervisor_agent
# from app.agents.weather import weather_agent

# from app.graph.router import (
#     ROUTE_MAP,
#     route_after_agent,
#     route_from_supervisor,
# )

# from app.graph.state import TravelState


# # =========================================================
# # Create Graph
# # =========================================================

# graph = StateGraph(TravelState)


# # =========================================================
# # Nodes
# # =========================================================

# graph.add_node("supervisor", supervisor_agent)
# graph.add_node("guardrail_blocked", guardrail_blocked_agent)

# graph.add_node("flight_agent", flight_agent)
# graph.add_node("hotel_agent", hotel_agent)
# graph.add_node("weather_agent", weather_agent)
# graph.add_node("budget_agent", budget_agent)

# graph.add_node("itinerary_agent", itinerary_agent)
# graph.add_node("human_approval", reviewer_agent)
# graph.add_node("final_agent", responder_agent)


# # =========================================================
# # Entry
# # =========================================================

# graph.add_edge(
#     START,
#     "supervisor",
# )


# # =========================================================
# # Supervisor Routing
# # =========================================================

# graph.add_conditional_edges(
#     "supervisor",
#     route_from_supervisor,
#     ROUTE_MAP,
# )


# # =========================================================
# # Specialist Agent Routing
# # =========================================================

# graph.add_conditional_edges(
#     "flight_agent",
#     route_after_agent("flight_agent"),
#     ROUTE_MAP,
# )

# graph.add_conditional_edges(
#     "hotel_agent",
#     route_after_agent("hotel_agent"),
#     ROUTE_MAP,
# )

# graph.add_conditional_edges(
#     "weather_agent",
#     route_after_agent("weather_agent"),
#     ROUTE_MAP,
# )

# graph.add_conditional_edges(
#     "budget_agent",
#     route_after_agent("budget_agent"),
#     ROUTE_MAP,
# )


# # =========================================================
# # Final Pipeline
# # =========================================================

# graph.add_edge(
#     "itinerary_agent",
#     "human_approval",
# )

# graph.add_edge(
#     "human_approval",
#     "final_agent",
# )

# graph.add_edge(
#     "final_agent",
#     END,
# )


# # =========================================================
# # Guardrail
# # =========================================================

# graph.add_edge(
#     "guardrail_blocked",
#     END,
# )


# # =========================================================
# # Compile WITHOUT Checkpointer
# # =========================================================

# travel_graph = graph.compile()








"""
LangGraph Workflow Builder for TripMate AI.
"""

from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from app.agents.budget import budget_agent
from app.agents.flight import flight_agent
from app.agents.guardrail import guardrail_blocked_agent
from app.agents.hotel import hotel_agent
from app.agents.itinerary import itinerary_agent
from app.agents.responder import responder_agent
from app.agents.supervisor import supervisor_agent
from app.agents.weather import weather_agent

from app.graph.router import (
    ROUTE_MAP,
    route_after_agent,
    route_from_supervisor,
)

from app.graph.state import TravelState


# =========================================================
# Create Graph
# =========================================================

graph = StateGraph(TravelState)


# =========================================================
# Nodes
# =========================================================

graph.add_node("supervisor", supervisor_agent)
graph.add_node("guardrail_blocked", guardrail_blocked_agent)

graph.add_node("flight_agent", flight_agent)
graph.add_node("hotel_agent", hotel_agent)
graph.add_node("weather_agent", weather_agent)
graph.add_node("budget_agent", budget_agent)

graph.add_node("itinerary_agent", itinerary_agent)
graph.add_node("final_agent", responder_agent)


# =========================================================
# Entry
# =========================================================

graph.add_edge(
    START,
    "supervisor",
)


# =========================================================
# Supervisor Routing
# =========================================================

graph.add_conditional_edges(
    "supervisor",
    route_from_supervisor,
    ROUTE_MAP,
)


# =========================================================
# Specialist Agent Routing
# =========================================================

graph.add_conditional_edges(
    "flight_agent",
    route_after_agent("flight_agent"),
    ROUTE_MAP,
)

graph.add_conditional_edges(
    "hotel_agent",
    route_after_agent("hotel_agent"),
    ROUTE_MAP,
)

graph.add_conditional_edges(
    "weather_agent",
    route_after_agent("weather_agent"),
    ROUTE_MAP,
)

graph.add_conditional_edges(
    "budget_agent",
    route_after_agent("budget_agent"),
    ROUTE_MAP,
)


# =========================================================
# Itinerary → Final Response
# =========================================================

graph.add_edge(
    "itinerary_agent",
    "final_agent",
)

graph.add_edge(
    "final_agent",
    END,
)


# =========================================================
# Guardrail
# =========================================================

graph.add_edge(
    "guardrail_blocked",
    END,
)


# =========================================================
# Compile
# =========================================================

travel_graph = graph.compile()