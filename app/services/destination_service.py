"""
Destination Extraction Service
"""

from __future__ import annotations

from app.core.logging import get_logger
from app.llm.groq_client import llm
from app.llm.prompts import DESTINATION_PROMPT, DESTINATION_SYSTEM_PROMPT

logger = get_logger(__name__)


def extract_destination(query: str) -> str:
    """
    Extract destination city/country from the user's travel request.
    """
    logger.info("Extracting destination...")

    response = llm.invoke(
        [
            ("system", DESTINATION_SYSTEM_PROMPT),
            ("human", DESTINATION_PROMPT.format(query=query)),
        ]
    )

    destination = str(response.content).strip()

    if not destination:
        raise ValueError("Unable to extract destination.")

    logger.info("Destination: %s", destination)
    return destination