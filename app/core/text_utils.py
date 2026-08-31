
from __future__ import annotations


def limit_text(
    value: object,
    max_chars: int = 4000,
) -> str:
    """
    Convert a value to string and safely limit its size.

    This prevents large MCP/search/agent outputs from
    consuming the entire LLM context window.
    """

    if value is None:
        return ""

    text = str(value).strip()

    if len(text) <= max_chars:
        return text

    return (
        text[:max_chars]
        + "\n\n[Content truncated to protect LLM context size.]"
    )

