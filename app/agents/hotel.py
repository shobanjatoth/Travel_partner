# """
# Hotel Specialist Agent
# """

# from __future__ import annotations

# from langchain_core.messages import AIMessage

# from app.core.logging import get_logger
# from app.graph.state import TravelState
# from app.mcp.tools.tavily import tavily_mcp_search

# logger = get_logger(__name__)


# async def hotel_agent(state: TravelState) -> TravelState:
#     """
#     Search hotels using Tavily MCP.
#     """
#     logger.info("Running Hotel Agent")

#     user_query = state.get("user_query", "")
#     query = f"Best hotels and stay options for: {user_query}"

#     try:
#         hotel_results = await tavily_mcp_search(query)
#     except Exception:
#         logger.exception("Hotel MCP search failed.")
#         hotel_results = (
#             "Live hotel search is currently unavailable.\n"
#             "Provide general hotel recommendations and suitable neighborhoods."
#         )

#     return {
#         "hotel_results": str(hotel_results),
#         "messages": [AIMessage(content="Hotel recommendations generated.")],
#         "llm_calls": state.get("llm_calls", 0) + 1,
#     }






"""
Hotel Specialist Agent
"""

from __future__ import annotations

from langchain_core.messages import AIMessage

from app.core.logging import get_logger
from app.core.text_utils import limit_text
from app.graph.state import TravelState
from app.mcp.tools.tavily import tavily_mcp_search

logger = get_logger(__name__)


async def hotel_agent(state: TravelState) -> TravelState:
    """
    Search hotels using Tavily MCP.

    Search output is deliberately limited before storing it
    in the shared graph state.
    """

    logger.info("Running Hotel Agent")

    user_query = limit_text(
        state.get("user_query", ""),
        max_chars=3000,
    )

    query = f"Best hotels and stay options for: {user_query}"

    try:
        hotel_results = await tavily_mcp_search(query)

        hotel_results = limit_text(
            hotel_results,
            max_chars=3500,
        )

    except Exception:
        logger.exception("Hotel MCP search failed.")

        hotel_results = (
            "Live hotel search is currently unavailable. "
            "Provide general hotel recommendations and suitable "
            "neighborhoods."
        )

    return {
        "hotel_results": hotel_results,
        "messages": [
            AIMessage(
                content="Hotel recommendations generated."
            )
        ],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }

