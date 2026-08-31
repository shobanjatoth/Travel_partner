# """
# Flight Specialist Agent
# """

# from __future__ import annotations

# from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

# from app.core.logging import get_logger
# from app.graph.state import TravelState
# from app.llm.groq_client import llm
# from app.llm.prompts import FLIGHT_AGENT_PROMPT
# from app.mcp.tools.tavily import tavily_mcp_search

# logger = get_logger(__name__)


# async def flight_agent(state: TravelState) -> TravelState:
#     """
#     Async flight agent node.
#     Gathers flight information via web search and formats flight choices.
#     """
#     logger.info("Running Flight Agent")
#     query = state.get("user_query", "")

#     try:
#         flight_search_results = await tavily_mcp_search(f"Flights for: {query}")

#         prompt = FLIGHT_AGENT_PROMPT.format(
#             query=query,
#             airport_data=str(flight_search_results)[:3000],
#             airline_data="See search results",
#         )

#         response = await llm.ainvoke(
#             [
#                 SystemMessage(content="You are a travel flight expert."),
#                 HumanMessage(content=prompt),
#             ]
#         )

#         result = str(response.content)

#     except Exception as exc:
#         logger.exception("Flight Agent Failed")
#         result = f"Flight information unavailable: {exc}"

#     return {
#         "flight_results": result,
#         "messages": [AIMessage(content="Flight recommendations generated.")],
#         "llm_calls": state.get("llm_calls", 0) + 1,
#     }




"""
Flight Specialist Agent
"""

from __future__ import annotations

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from app.core.logging import get_logger
from app.core.text_utils import limit_text
from app.graph.state import TravelState
from app.llm.groq_client import llm
from app.llm.prompts import FLIGHT_AGENT_PROMPT
from app.mcp.tools.tavily import tavily_mcp_search

logger = get_logger(__name__)


async def flight_agent(state: TravelState) -> TravelState:
    """
    Search and summarize flight information.

    Only a limited amount of search data and output is stored
    in the shared graph state.
    """

    logger.info("Running Flight Agent")

    query = limit_text(
        state.get("user_query", ""),
        max_chars=3000,
    )

    try:
        flight_search_results = await tavily_mcp_search(
            f"Flights for: {query}"
        )

        search_text = limit_text(
            flight_search_results,
            max_chars=3000,
        )

        prompt = FLIGHT_AGENT_PROMPT.format(
            query=query,
            airport_data=search_text,
            airline_data="Use the supplied search results.",
        )

        response = await llm.ainvoke(
            [
                SystemMessage(
                    content=(
                        "You are a travel flight expert. "
                        "Summarize only the most useful flight information. "
                        "Keep the response concise."
                    )
                ),
                HumanMessage(content=prompt),
            ]
        )

        result = limit_text(
            response.content,
            max_chars=3500,
        )

    except Exception as exc:
        logger.exception("Flight Agent Failed")

        result = (
            "Flight information is currently unavailable."
        )

    return {
        "flight_results": result,
        "messages": [
            AIMessage(
                content="Flight recommendations generated."
            )
        ],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }

