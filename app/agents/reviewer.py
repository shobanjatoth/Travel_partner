"""
Human Approval Node
"""

from __future__ import annotations

from langchain_core.messages import AIMessage
from langgraph.types import interrupt

from app.core.logging import get_logger
from app.graph.state import TravelState

logger = get_logger(__name__)


def reviewer_agent(state: TravelState) -> TravelState:
    """
    Human-in-the-loop review step using LangGraph interrupts.
    """
    logger.info("Waiting for human approval...")

    review = interrupt(
        {
            "question": "Approve this itinerary?",
            "draft_itinerary": state.get("itinerary", ""),
            "approval_request": state.get("approval_request", ""),
            "selected_agents": state.get("selected_agents", []),
            "supervisor_reasoning": state.get("supervisor_reasoning", ""),
            "expected_response": {
                "approved": True,
                "feedback": "Optional feedback string",
            },
        }
    )

    # Coerce response safely
    if isinstance(review, dict):
        is_approved = bool(review.get("approved", False))
        feedback = str(review.get("feedback", ""))
    else:
        is_approved = bool(review)
        feedback = ""

    return {
        "approved": is_approved,
        "human_feedback": feedback,
        "messages": [AIMessage(content="Human review completed.")],
    }