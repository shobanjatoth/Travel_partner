
"""
Itinerary Specialist Agent
"""

from __future__ import annotations

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from app.core.logging import get_logger
from app.core.text_utils import limit_text
from app.graph.state import TravelState
from app.llm.groq_client import llm
from app.llm.prompts import ITINERARY_AGENT_PROMPT

logger = get_logger(__name__)


async def itinerary_agent(state: TravelState) -> TravelState:
    """
    Generate a complete itinerary from specialist results.

    Only bounded specialist outputs are sent to the LLM.
    """

    logger.info("Running Itinerary Agent")

    query = limit_text(
        state.get("user_query", ""),
        max_chars=3000,
    )

    constraints = limit_text(
        state.get("trip_constraints", {}),
        max_chars=1500,
    )

    flight = limit_text(
        state.get("flight_results", ""),
        max_chars=2500,
    )

    hotel = limit_text(
        state.get("hotel_results", ""),
        max_chars=2500,
    )

    weather = limit_text(
        state.get("weather_results", ""),
        max_chars=2000,
    )

    budget = limit_text(
        state.get("budget_results", ""),
        max_chars=2500,
    )

    prompt = ITINERARY_AGENT_PROMPT.format(
        query=query,
        constraints=constraints,
        flight=flight,
        hotel=hotel,
        weather=weather,
        budget=budget,
    )

    response = await llm.ainvoke(
        [
            SystemMessage(
                content=(
                    "You are a travel itinerary planner. "
                    "Create a practical day-by-day itinerary. "
                    "Use only the supplied information. "
                    "Do not invent specific live prices or availability. "
                    "Keep the response concise."
                )
            ),
            HumanMessage(content=prompt),
        ]
    )

    itinerary = limit_text(
        response.content,
        max_chars=5000,
    )

    return {
        "itinerary": itinerary,
        "messages": [
            AIMessage(
                content="Itinerary generated."
            )
        ],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }


# """
# Itinerary Specialist Agent
# """

# from __future__ import annotations

# from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

# from app.core.logging import get_logger
# from app.graph.state import TravelState
# from app.llm.groq_client import llm
# from app.llm.prompts import ITINERARY_AGENT_PROMPT

# logger = get_logger(__name__)


# async def itinerary_agent(state: TravelState) -> TravelState:
#     """
#     Generate a complete travel itinerary based on all collected specialist data.
#     """
#     logger.info("Running Itinerary Agent")

#     # Match exact prompt template placeholders: query, constraints, flight, hotel, weather, budget
#     prompt = ITINERARY_AGENT_PROMPT.format(
#         query=state.get("user_query", ""),
#         constraints=state.get("trip_constraints", {}),
#         flight=state.get("flight_results", "No flight data available"),
#         hotel=state.get("hotel_results", "No hotel data available"),
#         weather=state.get("weather_results", "No weather data available"),
#         budget=state.get("budget_results", "No budget data available"),
#     )

#     response = await llm.ainvoke(
#         [
#             SystemMessage(
#                 content="You are a travel itinerary planner skilled at crafting detailed schedules."
#             ),
#             HumanMessage(content=prompt),
#         ]
#     )

#     return {
#         "itinerary": str(response.content),
#         "messages": [AIMessage(content="Itinerary generated.")],
#         "llm_calls": state.get("llm_calls", 0) + 1,
#     }