import pytest
from unittest.mock import patch
from app.agents.flight import flight_agent


@patch("app.agents.flight.llm")
def test_flight_agent_execution(mock_llm):
    mock_llm.invoke.return_value.content = "Flight options: Airline A - $500, Airline B - $450"

    state = {
        "user_query": "Find flights to Paris",
        "trip_constraints": {"destination": "Paris"},
    }

    result = flight_agent(state)

    assert "flight_results" in result
    assert "Airline A" in result["flight_results"]