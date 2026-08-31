import pytest
from app.graph.router import route_after_agent, route_from_supervisor


def test_route_from_supervisor_blocked():
    state = {"guardrail_allowed": False}
    assert route_from_supervisor(state) == "guardrail_blocked"


def test_route_from_supervisor_selected():
    state = {
        "guardrail_allowed": True,
        "selected_agents": ["flight_agent", "hotel_agent"],
    }
    assert route_from_supervisor(state) == "flight_agent"


def test_route_after_agent_sequence():
    state = {
        "selected_agents": ["flight_agent", "weather_agent"],
    }
    # After flight_agent, next selected in order is weather_agent
    route_fn = route_after_agent("flight_agent")
    assert route_fn(state) == "weather_agent"

    # After weather_agent, no more agents -> itinerary_agent
    route_fn_end = route_after_agent("weather_agent")
    assert route_fn_end(state) == "itinerary_agent"