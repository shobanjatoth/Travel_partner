# """
# Budget Specialist Agent
# """

# from __future__ import annotations

# from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

# from app.core.logging import get_logger
# from app.graph.state import TravelState
# from app.llm.groq_client import llm
# from app.llm.prompts import BUDGET_AGENT_PROMPT

# logger = get_logger(__name__)


# def detect_currency(query: str, constraints: dict) -> str:
#     """Detect currency symbol and name based on travel destination or query context."""
#     combined_text = f"{query} {constraints.get('destination', '')}".lower()

#     # Check for Indian travel destinations or currency keywords
#     indian_keywords = [
#         "india", "inr", "rupee", "rupees", "rs", "delhi", "mumbai",
#         "goa", "bangalore", "bengaluru", "chennai", "kolkata", "hyderabad",
#         "kerala", "jaipur", "manali", "shimla", "kashmir", "agra"
#     ]
#     if any(keyword in combined_text for keyword in indian_keywords):
#         return "₹ (INR)"

#     # Check for European destinations using Euros
#     euro_keywords = ["france", "paris", "germany", "italy", "spain", "euro", "eur"]
#     if any(keyword in combined_text for keyword in euro_keywords):
#         return "€ (EUR)"

#     # Default to USD for foreign/international travel
#     return "$ (USD)"


# async def budget_agent(state: TravelState) -> TravelState:
#     """
#     Perform budget analysis based on constraints and gathered travel options.
#     """
#     logger.info("Running Budget Agent")

#     query = state.get("user_query", "")
#     constraints = state.get("trip_constraints", {})
    
#     # Dynamically detect currency based on destination
#     currency = detect_currency(query, constraints)

#     # Match exact prompt template placeholders
#     prompt = BUDGET_AGENT_PROMPT.format(
#         query=query,
#         constraints=constraints,
#         flight=state.get("flight_results", "No flight data available"),
#         hotel=state.get("hotel_results", "No hotel data available"),
#         weather=state.get("weather_results", "No weather data available"),
#         currency=currency,
#     )

#     response = await llm.ainvoke(
#         [
#             SystemMessage(
#                 content=(
#                     "You are a travel budget analyst skilled at cost breakdowns. "
#                     f"Always calculate and express monetary values in {currency}."
#                 )
#             ),
#             HumanMessage(content=prompt),
#         ]
#     )

#     return {
#         "budget_results": str(response.content),
#         "messages": [AIMessage(content="Budget analysis generated.")],
#         "llm_calls": state.get("llm_calls", 0) + 1,
#     }





"""
Budget Specialist Agent
"""

from __future__ import annotations

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from app.core.logging import get_logger
from app.core.text_utils import limit_text
from app.graph.state import TravelState
from app.llm.groq_client import llm
from app.llm.prompts import BUDGET_AGENT_PROMPT

logger = get_logger(__name__)


def detect_currency(query: str, constraints: dict) -> str:
    """
    Detect currency from travel destination/query.
    """

    combined_text = (
        f"{query} {constraints.get('destination', '')}"
    ).lower()

    indian_keywords = [
        "india",
        "inr",
        "rupee",
        "rupees",
        "rs",
        "delhi",
        "mumbai",
        "goa",
        "bangalore",
        "bengaluru",
        "chennai",
        "kolkata",
        "hyderabad",
        "kerala",
        "jaipur",
        "manali",
        "shimla",
        "kashmir",
        "agra",
    ]

    if any(
        keyword in combined_text
        for keyword in indian_keywords
    ):
        return "₹ (INR)"

    euro_keywords = [
        "france",
        "paris",
        "germany",
        "italy",
        "spain",
        "euro",
        "eur",
    ]

    if any(
        keyword in combined_text
        for keyword in euro_keywords
    ):
        return "€ (EUR)"

    return "$ (USD)"


async def budget_agent(state: TravelState) -> TravelState:
    """
    Analyze the travel budget using summarized specialist data.
    """

    logger.info("Running Budget Agent")

    query = limit_text(
        state.get("user_query", ""),
        max_chars=3000,
    )

    constraints = state.get(
        "trip_constraints",
        {},
    )

    currency = detect_currency(
        query,
        constraints,
    )

    prompt = BUDGET_AGENT_PROMPT.format(
        query=query,
        constraints=limit_text(
            constraints,
            max_chars=1500,
        ),
        flight=limit_text(
            state.get("flight_results", ""),
            max_chars=2000,
        ),
        hotel=limit_text(
            state.get("hotel_results", ""),
            max_chars=2000,
        ),
        weather=limit_text(
            state.get("weather_results", ""),
            max_chars=1500,
        ),
        currency=currency,
    )

    response = await llm.ainvoke(
        [
            SystemMessage(
                content=(
                    "You are a travel budget analyst. "
                    f"Use {currency}. "
                    "Keep the analysis concise and practical."
                )
            ),
            HumanMessage(content=prompt),
        ]
    )

    result = limit_text(
        response.content,
        max_chars=3000,
    )

    return {
        "budget_results": result,
        "messages": [
            AIMessage(
                content="Budget analysis generated."
            )
        ],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }

