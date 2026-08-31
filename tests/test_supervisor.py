import pytest
from unittest.mock import patch, MagicMock
from app.agents.supervisor import supervisor_agent


@patch("app.agents.supervisor.llm")
def test_supervisor_agent_valid_query(mock_llm):
    # Mock LLM structured response
    mock_response = MagicMock()
    mock_response.guardrail_allowed = True
    mock_response.guardrail_reason = ""
    mock_response.selected_agents = ["flight_agent", "hotel_agent"]
    mock_response.trip_constraints = {"destination": "Tokyo", "days": 5}
    mock_response.reasoning = "User requested flights and hotels for Tokyo."

    mock_llm.with_structured_output.return_value.invoke.return_value = mock_response

    state = {"user_query": "Plan a 5-day trip to Tokyo with flights and hotels."}
    result = supervisor_agent(state)

    assert result["guardrail_allowed"] is True
    assert result["selected_agents"] == ["flight_agent", "hotel_agent"]
    assert result["trip_constraints"]["destination"] == "Tokyo"