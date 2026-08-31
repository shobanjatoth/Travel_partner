import pytest
from unittest.mock import patch
from app.agents.budget import budget_agent


@patch("app.agents.budget.llm")
def test_budget_agent_execution(mock_llm):
    mock_llm.invoke.return_value.content = "Total estimated budget: $1200 USD."

    state = {
        "user_query": "Estimate budget for 3 days in London",
        "trip_constraints": {"destination": "London", "days": 3},
    }

    result = budget_agent(state)

    assert "budget_results" in result
    assert "$1200 USD" in result["budget_results"]