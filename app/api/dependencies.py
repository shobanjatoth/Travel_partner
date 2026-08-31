"""
Shared FastAPI Dependencies and Helpers
"""

from __future__ import annotations

from fastapi import HTTPException


def validate_feedback(
    approved: bool,
    feedback: str,
) -> None:
    """
    Require revision feedback when rejecting an itinerary.
    """
    if not approved and not feedback.strip():
        raise HTTPException(
            status_code=400,
            detail="Please provide revision feedback when rejecting the itinerary.",
        )