
"""
Final Responder Agent
"""

from __future__ import annotations

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from app.core.logging import get_logger
from app.core.text_utils import limit_text
from app.graph.state import TravelState
from app.llm.groq_client import llm
from app.llm.prompts import FINAL_RESPONSE_PROMPT

logger = get_logger(__name__)


async def responder_agent(state: TravelState) -> TravelState:
    """
    Generate the final response from the approved itinerary.

    The responder intentionally receives only the itinerary,
    user query, and human feedback instead of all specialist
    outputs. This keeps the LLM context small.
    """

    logger.info("Running Responder Agent")

    query = limit_text(
        state.get("user_query", ""),
        max_chars=2500,
    )

    itinerary = limit_text(
        state.get("itinerary", ""),
        max_chars=5000,
    )

    feedback = limit_text(
        state.get("human_feedback", "None"),
        max_chars=1500,
    )

    prompt = FINAL_RESPONSE_PROMPT.format(
        query=query,
        itinerary=itinerary,
        feedback=feedback,
    )

    response = await llm.ainvoke(
        [
            SystemMessage(
                content=(
                    "You are the final travel assistant. "
                    "Present the approved itinerary clearly. "
                    "Incorporate human feedback when provided. "
                    "Do not invent unavailable information."
                )
            ),
            HumanMessage(content=prompt),
        ]
    )

    final_content = limit_text(
        response.content,
        max_chars=6000,
    )

    return {
        "final_response": final_content,
        "messages": [
            AIMessage(content=final_content)
        ],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }











# """
# Final Responder Agent
# """

# from __future__ import annotations

# from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

# from app.core.logging import get_logger
# from app.graph.state import TravelState
# from app.llm.groq_client import llm
# from app.llm.prompts import FINAL_RESPONSE_PROMPT

# logger = get_logger(__name__)


# async def responder_agent(state: TravelState) -> TravelState:
#     """
#     Generate the final consolidated response after human approval or revision.
#     """
#     logger.info("Running Responder Agent")

#     # Match exact prompt template placeholders: query, flight, hotel, weather, budget, itinerary, feedback
#     prompt = FINAL_RESPONSE_PROMPT.format(
#         query=state.get("user_query", ""),
#         flight=state.get("flight_results", "No flight details"),
#         hotel=state.get("hotel_results", "No hotel details"),
#         weather=state.get("weather_results", "No weather details"),
#         budget=state.get("budget_results", "No budget details"),
#         itinerary=state.get("itinerary", "No itinerary generated"),
#         feedback=state.get("human_feedback", "None"),
#     )

#     response = await llm.ainvoke(
#         [
#             SystemMessage(
#                 content="You are a primary travel assistant summarizing the complete approved trip plan."
#             ),
#             HumanMessage(content=prompt),
#         ]
#     )

#     final_content = str(response.content)

#     return {
#         "final_response": final_content,
#         "messages": [AIMessage(content=final_content)],
#         "llm_calls": state.get("llm_calls", 0) + 1,
#     }