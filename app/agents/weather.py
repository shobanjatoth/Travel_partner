# """
# Weather Specialist Agent
# """

# from __future__ import annotations

# from langchain_core.messages import AIMessage

# from app.core.logging import get_logger
# from app.graph.state import TravelState
# from app.mcp.tools.weather import forecast_mcp_search, weather_mcp_search
# from app.services.destination_service import extract_destination

# logger = get_logger(__name__)


# async def weather_agent(state: TravelState) -> TravelState:
#     """
#     Fetch live weather and forecast information using Weather MCP.
#     """
#     logger.info("Running Weather Agent")

#     user_query = state.get("user_query", "")
#     city = extract_destination(user_query)

#     try:
#         weather = await weather_mcp_search(city)
#         forecast = await forecast_mcp_search(city)

#         weather_results = (
#             f"Current Weather:\n{weather}\n\nForecast:\n{forecast}"
#         )
#     except Exception:
#         logger.exception("Weather MCP failed.")
#         weather_results = (
#             f"Live weather for '{city}' is unavailable.\n"
#             "Provide general seasonal guidance based on historical climate."
#         )

#     return {
#         "weather_results": weather_results,
#         "messages": [AIMessage(content="Weather data generated.")],
#         "llm_calls": state.get("llm_calls", 0) + 1,
#     }







"""
Weather Specialist Agent
"""

from __future__ import annotations

from langchain_core.messages import AIMessage

from app.core.logging import get_logger
from app.core.text_utils import limit_text
from app.graph.state import TravelState
from app.mcp.tools.weather import (
    forecast_mcp_search,
    weather_mcp_search,
)
from app.services.destination_service import extract_destination

logger = get_logger(__name__)


async def weather_agent(state: TravelState) -> TravelState:
    """
    Fetch live weather and forecast information.
    """

    logger.info("Running Weather Agent")

    user_query = limit_text(
        state.get("user_query", ""),
        max_chars=3000,
    )

    city = extract_destination(user_query)

    try:
        weather = await weather_mcp_search(city)
        forecast = await forecast_mcp_search(city)

        weather_results = (
            f"Current Weather:\n"
            f"{limit_text(weather, 1500)}\n\n"
            f"Forecast:\n"
            f"{limit_text(forecast, 2000)}"
        )

    except Exception:
        logger.exception("Weather MCP failed.")

        weather_results = (
            f"Live weather for '{city}' is unavailable. "
            "Provide general seasonal guidance."
        )

    return {
        "weather_results": weather_results,
        "messages": [
            AIMessage(
                content="Weather data generated."
            )
        ],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }

