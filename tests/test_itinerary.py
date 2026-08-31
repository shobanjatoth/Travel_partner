import pytest
from unittest.mock import patch
from app.agents.itinerary import itinerary_agent


@patch("app.agents.itinerary.llm")
def test_itinerary_agent_synthesis(mock_llm):
    mock_llm.invoke.return_value.content = "Day 1: Arrival & Hotel check-in\nDay 2: City tour"

    state = {
        "flight_results": "Flight A - $500",
        "hotel_results": "Hotel B - $150/night",
        "weather_results": "Sunny 25°C",
        "budget_results": "Estimated total: $1000",
    }

    result = itinerary_agent(state)

    assert "itinerary" in result
    assert "Day 1" in result["itinerary"]