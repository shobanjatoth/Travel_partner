"""
Centralized Groq LLM client.
"""

from __future__ import annotations

from langchain_groq import ChatGroq

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class GroqClient:
    """
    Wrapper around ChatGroq.
    """

    def __init__(self) -> None:
        self._llm = ChatGroq(
            model=settings.GROQ_MODEL,
            api_key=settings.GROQ_API_KEY or "dummy_key",
            temperature=0,
        )

        logger.info(
            "Groq client initialized using model '%s'.",
            settings.GROQ_MODEL,
        )

    @property
    def client(self) -> ChatGroq:
        return self._llm


groq_client = GroqClient()
llm = groq_client.client