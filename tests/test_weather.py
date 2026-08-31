import pytest
from unittest.mock import patch
from app.agents.weather import weather_agent


@patch("app.agents.weather.llm")
def test_weather_agent_execution(mock_llm):
    mock_llm.invoke.return_value.content = "Expected weather in Tokyo: Sunny, 22°C."

    state = {
        "user_query": "What's the weather in Tokyo?",
        "trip_constraints": {"destination": "Tokyo"},
    }

    result = weather_agent(state)

    assert "weather_results" in result
    assert "Sunny" in result["weather_results"]