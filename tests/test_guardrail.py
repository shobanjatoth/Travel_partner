import pytest
from app.agents.guardrail import guardrail_blocked_agent


def test_guardrail_blocked_agent():
    state = {
        "guardrail_reason": "Query contains unsafe content or non-travel topic."
    }

    result = guardrail_blocked_agent(state)

    assert "final_response" in result
    assert "unsafe" in result["final_response"].lower() or "cannot assist" in result["final_response"].lower()
    assert result.get("guardrail_allowed") is False