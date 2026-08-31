"""
LLM response parsing utilities.
"""

from __future__ import annotations

import json
import re
from typing import Any

from app.core.exceptions import LLMResponseError


def extract_json(text: str) -> dict[str, Any]:
    """
    Extract the first valid JSON object returned by the LLM,
    handling standard JSON strings as well as markdown-fenced block quotes.
    """
    cleaned_text = re.sub(r"```(?:json)?\n?", "", text).strip("` \n\r")

    start = cleaned_text.find("{")
    end = cleaned_text.rfind("}")

    if start == -1 or end == -1:
        raise LLMResponseError("No JSON object found in LLM response.")

    json_str = cleaned_text[start : end + 1]

    try:
        return json.loads(json_str)
    except json.JSONDecodeError as exc:
        raise LLMResponseError(
            f"Invalid JSON returned by LLM: {exc}"
        ) from exc


def extract_text(response: Any) -> str:
    """
    Convert LangChain response object into plain text.
    """
    content = getattr(response, "content", response)
    return str(content).strip()