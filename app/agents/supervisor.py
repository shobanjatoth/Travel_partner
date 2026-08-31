# """
# Supervisor Agent
# """

# from __future__ import annotations

# from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

# from app.core.constants import AGENT_ORDER, KNOWN_AGENTS
# from app.core.logging import get_logger
# from app.graph.state import TravelState, empty_constraints
# from app.llm.groq_client import llm
# from app.llm.parser import extract_json
# from app.llm.prompts import INPUT_GUARDRAIL_PROMPT, SUPERVISOR_PROMPT

# logger = get_logger(__name__)


# def supervisor_agent(state: TravelState) -> TravelState:
#     """
#     Supervisor node.
#     1. Validate request using guardrail prompt.
#     2. Select specialist agents.
#     3. Extract trip constraints.
#     """
#     logger.info("Running Supervisor Agent")

#     query = state.get("user_query", "")
#     llm_calls = state.get("llm_calls", 0)

#     # Guardrail Check
#     try:
#         response = llm.invoke(
#             [
#                 SystemMessage(content="You are a travel planning request evaluator."),
#                 HumanMessage(content=INPUT_GUARDRAIL_PROMPT.format(query=query)),
#             ]
#         )

#         result = extract_json(str(response.content))
#         allowed = bool(result.get("allowed", True))
#         reason = str(result.get("reason", "")).strip()
#         llm_calls += 1

#     except Exception:
#         logger.exception("Guardrail check failed; falling back to allowed.")
#         allowed = True
#         reason = "Guardrail fallback."

#     if not allowed:
#         return {
#             "guardrail_allowed": False,
#             "guardrail_reason": reason,
#             "selected_agents": [],
#             "trip_constraints": empty_constraints(),
#             "supervisor_reasoning": reason,
#             "final_response": reason,
#             "messages": [AIMessage(content=reason)],
#             "llm_calls": llm_calls,
#         }

#     # Supervisor Planning
#     try:
#         response = llm.invoke(
#             [
#                 SystemMessage(content="You are the supervisor of a travel system."),
#                 HumanMessage(content=SUPERVISOR_PROMPT.format(query=query)),
#             ]
#         )

#         result = extract_json(str(response.content))
#         requested_agents = result.get("selected_agents", [])

#         selected = [
#             agent
#             for agent in AGENT_ORDER
#             if agent in requested_agents and agent in KNOWN_AGENTS
#         ]

#         if "itinerary_agent" not in selected:
#             selected.append("itinerary_agent")

#         constraints = empty_constraints()
#         constraints.update(result.get("trip_constraints", {}))
#         reasoning = result.get("reasoning", "")
#         llm_calls += 1

#     except Exception:
#         logger.exception("Supervisor agent failed; using fallback plan.")
#         selected = AGENT_ORDER.copy()
#         constraints = empty_constraints()
#         reasoning = "Supervisor fallback selected full workflow."

#     logger.info("Selected Agents: %s", selected)

#     return {
#         "guardrail_allowed": True,
#         "guardrail_reason": reason,
#         "selected_agents": selected,
#         "trip_constraints": constraints,
#         "supervisor_reasoning": reasoning,
#         "messages": [AIMessage(content="Supervisor created execution plan.")],
#         "llm_calls": llm_calls,
#     }



from __future__ import annotations

from typing import Any

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from app.core.constants import AGENT_ORDER, KNOWN_AGENTS
from app.core.logging import get_logger
from app.graph.state import TravelState, empty_constraints
from app.llm.groq_client import llm
from app.llm.parser import extract_json
from app.llm.prompts import INPUT_GUARDRAIL_PROMPT, SUPERVISOR_PROMPT

logger = get_logger(__name__)


def _safe_extract_json(content: Any) -> dict[str, Any]:
    """
    Safely extract a JSON object from an LLM response.

    Raises:
        ValueError: If the response is not a valid JSON object.
    """
    if content is None:
        raise ValueError("LLM returned empty response.")

    text = str(content).strip()

    if not text:
        raise ValueError("LLM returned empty content.")

    result = extract_json(text)

    if not isinstance(result, dict):
        raise ValueError(
            f"Expected JSON object, got {type(result).__name__}."
        )

    return result


def _select_agents(requested_agents: Any) -> list[str]:
    """
    Validate and order agents returned by the supervisor LLM.

    Only agents present in AGENT_ORDER and KNOWN_AGENTS are allowed.
    Itinerary agent is always included because every travel request
    requires an itinerary.
    """

    if not isinstance(requested_agents, list):
        requested_agents = []

    requested_agents = {
        str(agent).strip()
        for agent in requested_agents
        if isinstance(agent, str)
    }

    selected = [
        agent
        for agent in AGENT_ORDER
        if agent in requested_agents and agent in KNOWN_AGENTS
    ]

    # Every valid travel workflow must contain itinerary generation.
    if "itinerary_agent" in KNOWN_AGENTS and "itinerary_agent" not in selected:
        selected.append("itinerary_agent")

    return selected


def _build_fallback_plan() -> tuple[list[str], dict[str, Any], str]:
    """
    Return a safe deterministic supervisor fallback.
    """

    selected = [
        agent
        for agent in AGENT_ORDER
        if agent in KNOWN_AGENTS
    ]

    if "itinerary_agent" in KNOWN_AGENTS and "itinerary_agent" not in selected:
        selected.append("itinerary_agent")

    return (
        selected,
        empty_constraints(),
        "Supervisor could not parse the LLM response. "
        "Fallback workflow selected.",
    )


def _validate_constraints(value: Any) -> dict[str, Any]:
    """
    Validate trip constraints returned by the LLM.

    Only dictionaries are accepted. Invalid values are ignored.
    """

    constraints = empty_constraints()

    if isinstance(value, dict):
        constraints.update(value)

    return constraints


def _run_guardrail(query: str) -> tuple[bool, str, int]:
    """
    Run the travel-request guardrail.

    Returns:
        allowed, reason, llm_calls
    """

    try:
        response = llm.invoke(
            [
                SystemMessage(
                    content=(
                        "You are a strict travel request guardrail. "
                        "Return ONLY valid JSON. "
                        "Do not use markdown. "
                        "Do not add explanations outside JSON."
                    )
                ),
                HumanMessage(
                    content=INPUT_GUARDRAIL_PROMPT.format(query=query)
                ),
            ]
        )

        result = _safe_extract_json(response.content)

        allowed = result.get("allowed", False)
        reason = result.get("reason", "")

        if not isinstance(allowed, bool):
            allowed = False

        if not isinstance(reason, str):
            reason = str(reason)

        return allowed, reason.strip(), 1

    except Exception:
        logger.exception("Guardrail LLM call failed.")

        # Fail closed for the guardrail.
        return (
            False,
            "I can only help with travel planning requests.",
            1,
        )


def _run_supervisor(
    query: str,
) -> tuple[list[str], dict[str, Any], str, int]:
    """
    Run the supervisor planning LLM.

    Returns:
        selected_agents,
        trip_constraints,
        reasoning,
        llm_calls
    """

    try:
        response = llm.invoke(
            [
                SystemMessage(
                    content=(
                        "You are the supervisor of a travel planning system.\n\n"
                        "Your job is to select specialist agents and extract "
                        "trip constraints.\n\n"
                        "IMPORTANT:\n"
                        "Return ONLY valid JSON.\n"
                        "Do NOT use markdown fences.\n"
                        "Do NOT include explanations outside JSON.\n"
                        "Use double quotes for JSON keys and string values.\n"
                        "Ensure every object and array is properly closed."
                    )
                ),
                HumanMessage(
                    content=SUPERVISOR_PROMPT.format(query=query)
                ),
            ]
        )

        result = _safe_extract_json(response.content)

        requested_agents = result.get("selected_agents", [])
        constraints_data = result.get("trip_constraints", {})
        reasoning = result.get("reasoning", "")

        selected = _select_agents(requested_agents)

        constraints = _validate_constraints(constraints_data)

        if not isinstance(reasoning, str):
            reasoning = str(reasoning)

        # If the model returned no valid agents, use deterministic fallback.
        if not selected:
            logger.warning(
                "Supervisor returned no valid agents. "
                "Using fallback workflow."
            )

            selected, constraints, fallback_reason = _build_fallback_plan()

            return (
                selected,
                constraints,
                fallback_reason,
                1,
            )

        return (
            selected,
            constraints,
            reasoning.strip(),
            1,
        )

    except Exception:
        logger.exception(
            "Supervisor LLM planning failed. "
            "Using deterministic fallback workflow."
        )

        selected, constraints, reasoning = _build_fallback_plan()

        return (
            selected,
            constraints,
            reasoning,
            1,
        )


def supervisor_agent(state: TravelState) -> TravelState:
    """
    Supervisor node for the travel planning graph.

    Responsibilities:
        1. Validate whether the user request is travel-related.
        2. Select specialist agents.
        3. Extract trip constraints.
        4. Provide a deterministic fallback if the LLM fails.
        5. Never allow malformed LLM JSON to crash the graph.
    """

    logger.info("Running Supervisor Agent")

    query = str(state.get("user_query", "")).strip()
    llm_calls = int(state.get("llm_calls", 0))

    # ------------------------------------------------------------------
    # 1. Empty query protection
    # ------------------------------------------------------------------

    if not query:
        reason = "Please provide a travel-related request."

        logger.warning("Supervisor received an empty user query.")

        return {
            "guardrail_allowed": False,
            "guardrail_reason": reason,
            "selected_agents": [],
            "trip_constraints": empty_constraints(),
            "supervisor_reasoning": reason,
            "final_response": reason,
            "messages": [
                AIMessage(content=reason)
            ],
            "llm_calls": llm_calls,
        }

    # ------------------------------------------------------------------
    # 2. Guardrail
    # ------------------------------------------------------------------

    allowed, guardrail_reason, guardrail_calls = _run_guardrail(query)

    llm_calls += guardrail_calls

    logger.info(
        "Guardrail result: allowed=%s reason=%s",
        allowed,
        guardrail_reason,
    )

    if not allowed:
        reason = (
            guardrail_reason
            or "I can only help with travel planning requests."
        )

        return {
            "guardrail_allowed": False,
            "guardrail_reason": reason,
            "selected_agents": [],
            "trip_constraints": empty_constraints(),
            "supervisor_reasoning": reason,
            "final_response": reason,
            "messages": [
                AIMessage(content=reason)
            ],
            "llm_calls": llm_calls,
        }

    # ------------------------------------------------------------------
    # 3. Supervisor planning
    # ------------------------------------------------------------------

    (
        selected,
        constraints,
        reasoning,
        supervisor_calls,
    ) = _run_supervisor(query)

    llm_calls += supervisor_calls

    logger.info(
        "Selected Agents: %s",
        selected,
    )

    logger.info(
        "Trip Constraints: %s",
        constraints,
    )

    # ------------------------------------------------------------------
    # 4. Return state
    # ------------------------------------------------------------------

    return {
        "guardrail_allowed": True,
        "guardrail_reason": guardrail_reason,
        "selected_agents": selected,
        "trip_constraints": constraints,
        "supervisor_reasoning": reasoning,
        "messages": [
            AIMessage(
                content="Supervisor created the travel execution plan."
            )
        ],
        "llm_calls": llm_calls,
    }

