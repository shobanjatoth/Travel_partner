

# """
# Travel Service

# Acts as the interface between FastAPI and LangGraph.
# """

# from __future__ import annotations

# import uuid
# from typing import Any

# from langchain_core.messages import HumanMessage
# from langgraph.types import Command

# from app.core.constants import EMPTY_CONSTRAINTS
# from app.graph.builder import travel_graph


# def _interrupt_payload(result: dict[str, Any]) -> dict[str, Any] | None:
#     """
#     Extracts the interrupt state from the LangGraph execution result, if present.
#     """
#     interrupts = result.get("__interrupt__", [])
#     if not interrupts:
#         return None

#     first = interrupts[0]
#     payload = getattr(first, "value", first)

#     if isinstance(payload, dict):
#         return payload

#     return {"value": payload}


# def _serialize_result(result: dict[str, Any], thread_id: str) -> dict[str, Any]:
#     """
#     Formats the graph state and interrupt payloads into a clean FastAPI response dictionary.
#     """
#     messages = result.get("messages", [])
#     last_message = messages[-1].content if messages else ""
#     interrupt = _interrupt_payload(result)

#     answer = result.get("final_response") or last_message

#     if interrupt:
#         answer = interrupt.get("draft_itinerary", answer)

#     return {
#         "thread_id": thread_id,
#         "answer": answer,
#         "requires_approval": interrupt is not None,
#         "approval_request": (
#             interrupt.get("approval_request", "")
#             if interrupt
#             else result.get("approval_request", "")
#         ),
#         "flight_results": result.get("flight_results", ""),
#         "hotel_results": result.get("hotel_results", ""),
#         "weather_results": result.get("weather_results", ""),
#         "budget_results": result.get("budget_results", ""),
#         "itinerary": (
#             interrupt.get("draft_itinerary", "")
#             if interrupt
#             else result.get("itinerary", "")
#         ),
#         "selected_agents": result.get("selected_agents", []),
#         "trip_constraints": result.get("trip_constraints", {}),
#         "supervisor_reasoning": result.get("supervisor_reasoning", ""),
#         "guardrail_allowed": result.get("guardrail_allowed", True),
#         "guardrail_reason": result.get("guardrail_reason", ""),
#         "approved": result.get("approved"),
#         "human_feedback": result.get("human_feedback", ""),
#         "llm_calls": result.get("llm_calls", 0),
#     }


# async def run_travel_agent(
#     user_input: str,
#     thread_id: str | None = None,
# ) -> dict[str, Any]:
#     """
#     Initiates a new travel agent execution thread with initial user state.
#     """
#     if thread_id is None:
#         thread_id = f"user_{uuid.uuid4().hex}"

#     config = {"configurable": {"thread_id": thread_id}}

#     result = await travel_graph.ainvoke(
#         {
#             "messages": [HumanMessage(content=user_input)],
#             "user_query": user_input,
#             "guardrail_allowed": True,
#             "guardrail_reason": "",
#             "selected_agents": [],
#             "trip_constraints": EMPTY_CONSTRAINTS.copy(),
#             "supervisor_reasoning": "",
#             "flight_results": "",
#             "hotel_results": "",
#             "weather_results": "",
#             "budget_results": "",
#             "itinerary": "",
#             "approval_request": "",
#             "approved": False,
#             "human_feedback": "",
#             "final_response": "",
#             "llm_calls": 0,
#         },
#         config=config,
#     )

#     return _serialize_result(result, thread_id)


# async def resume_travel_agent(
#     thread_id: str,
#     approved: bool,
#     feedback: str = "",
# ) -> dict[str, Any]:
#     """
#     Resumes an interrupted travel workflow (Human-in-the-Loop) using LangGraph Commands.
#     """
#     config = {"configurable": {"thread_id": thread_id}}

#     result = await travel_graph.ainvoke(
#         Command(
#             resume={
#                 "approved": approved,
#                 "feedback": feedback.strip(),
#             }
#         ),
#         config=config,
#     )

#     return _serialize_result(result, thread_id)











# """
# Travel Service

# Acts as the interface between FastAPI and LangGraph execution.
# """

# from __future__ import annotations

# import uuid
# from typing import Any

# from langchain_core.messages import HumanMessage
# from langgraph.types import Command

# from app.core.constants import EMPTY_CONSTRAINTS
# from app.graph.builder import travel_graph


# def _interrupt_payload(result: dict[str, Any]) -> dict[str, Any] | None:
#     """
#     Extracts the interrupt state from the LangGraph execution result, if present.
#     """
#     interrupts = result.get("__interrupt__", [])
#     if not interrupts:
#         return None

#     first = interrupts[0]
#     payload = getattr(first, "value", first)

#     if isinstance(payload, dict):
#         return payload

#     return {"value": payload}


# def _serialize_result(result: dict[str, Any], thread_id: str) -> dict[str, Any]:
#     """
#     Formats the graph state and interrupt payloads into a clean FastAPI response dictionary.
#     """
#     messages = result.get("messages", [])
#     last_message = messages[-1].content if messages else ""
#     interrupt = _interrupt_payload(result)

#     answer = result.get("final_response") or last_message

#     if interrupt:
#         answer = interrupt.get("draft_itinerary", answer)

#     return {
#         "thread_id": thread_id,
#         "answer": answer,
#         "requires_approval": interrupt is not None,
#         "approval_request": (
#             interrupt.get("approval_request", "")
#             if interrupt
#             else result.get("approval_request", "")
#         ),
#         "flight_results": result.get("flight_results", ""),
#         "hotel_results": result.get("hotel_results", ""),
#         "weather_results": result.get("weather_results", ""),
#         "budget_results": result.get("budget_results", ""),
#         "itinerary": (
#             interrupt.get("draft_itinerary", "")
#             if interrupt
#             else result.get("itinerary", "")
#         ),
#         "selected_agents": result.get("selected_agents", []),
#         "trip_constraints": result.get("trip_constraints", {}),
#         "supervisor_reasoning": result.get("supervisor_reasoning", ""),
#         "guardrail_allowed": result.get("guardrail_allowed", True),
#         "guardrail_reason": result.get("guardrail_reason", ""),
#         "approved": result.get("approved"),
#         "human_feedback": result.get("human_feedback", ""),
#         "llm_calls": result.get("llm_calls", 0),
#     }


# async def run_travel_agent(
#     user_input: str,
#     thread_id: str | None = None,
# ) -> dict[str, Any]:
#     """
#     Initiates a new travel agent execution thread with initial user state.
#     """
#     if thread_id is None:
#         thread_id = f"user_{uuid.uuid4().hex}"

#     config = {"configurable": {"thread_id": thread_id}}

#     result = await travel_graph.ainvoke(
#         {
#             "messages": [HumanMessage(content=user_input)],
#             "user_query": user_input,
#             "guardrail_allowed": True,
#             "guardrail_reason": "",
#             "selected_agents": [],
#             "trip_constraints": EMPTY_CONSTRAINTS.copy(),
#             "supervisor_reasoning": "",
#             "flight_results": "",
#             "hotel_results": "",
#             "weather_results": "",
#             "budget_results": "",
#             "itinerary": "",
#             "approval_request": "",
#             "approved": False,
#             "human_feedback": "",
#             "final_response": "",
#             "llm_calls": 0,
#         },
#         config=config,
#     )

#     return _serialize_result(result, thread_id)


# async def resume_travel_agent(
#     thread_id: str,
#     approved: bool,
#     feedback: str = "",
# ) -> dict[str, Any]:
#     """
#     Resumes an interrupted travel workflow (Human-in-the-Loop) using LangGraph Commands.
#     """
#     config = {"configurable": {"thread_id": thread_id}}

#     result = await travel_graph.ainvoke(
#         Command(
#             resume={
#                 "approved": approved,
#                 "feedback": feedback.strip(),
#             }
#         ),
#         config=config,
#     )

#     return _serialize_result(result, thread_id)




"""
Travel Service

Acts as the interface between FastAPI and LangGraph execution.
"""

from __future__ import annotations

import uuid
from typing import Any

from langchain_core.messages import HumanMessage
from langgraph.types import Command

from app.core.constants import EMPTY_CONSTRAINTS
from app.graph.builder import travel_graph


# =========================================================
# Interrupt Handling
# =========================================================

def _interrupt_payload(
    result: dict[str, Any],
) -> dict[str, Any] | None:
    """
    Extract the first LangGraph interrupt payload.

    LangGraph stores interrupts under __interrupt__.
    """

    interrupts = result.get("__interrupt__")

    if not interrupts:
        return None

    first = interrupts[0]

    # LangGraph Interrupt objects expose their payload
    # through the `value` attribute.
    payload = getattr(first, "value", first)

    if isinstance(payload, dict):
        return payload

    return {
        "value": payload,
    }


# =========================================================
# Result Serialization
# =========================================================

def _serialize_result(
    result: dict[str, Any],
    thread_id: str,
) -> dict[str, Any]:
    """
    Convert LangGraph state into the response format
    expected by the FastAPI routes.
    """

    messages = result.get("messages") or []

    last_message = ""

    if messages:
        last = messages[-1]

        content = getattr(
            last,
            "content",
            "",
        )

        if isinstance(content, str):
            last_message = content
        else:
            last_message = str(content)

    interrupt = _interrupt_payload(result)

    # -----------------------------------------------------
    # Determine answer
    # -----------------------------------------------------

    answer = (
        result.get("final_response")
        or last_message
    )

    # If workflow is waiting for human approval,
    # show the draft itinerary as the answer.
    if interrupt:
        answer = (
            interrupt.get("draft_itinerary")
            or answer
        )

    # -----------------------------------------------------
    # Approval request
    # -----------------------------------------------------

    if interrupt:
        approval_request = (
            interrupt.get("approval_request")
            or result.get("approval_request")
            or ""
        )
    else:
        approval_request = (
            result.get("approval_request")
            or ""
        )

    # -----------------------------------------------------
    # Itinerary
    # -----------------------------------------------------

    if interrupt:
        itinerary = (
            interrupt.get("draft_itinerary")
            or result.get("itinerary")
            or ""
        )
    else:
        itinerary = (
            result.get("itinerary")
            or ""
        )

    # -----------------------------------------------------
    # Return API response
    # -----------------------------------------------------

    return {
        "thread_id": thread_id,

        "answer": answer,

        "requires_approval": (
            interrupt is not None
        ),

        "approval_request": approval_request,

        "flight_results": (
            result.get("flight_results")
            or ""
        ),

        "hotel_results": (
            result.get("hotel_results")
            or ""
        ),

        "weather_results": (
            result.get("weather_results")
            or ""
        ),

        "budget_results": (
            result.get("budget_results")
            or ""
        ),

        "itinerary": itinerary,

        "selected_agents": (
            result.get("selected_agents")
            or []
        ),

        "trip_constraints": (
            result.get("trip_constraints")
            or {}
        ),

        "supervisor_reasoning": (
            result.get("supervisor_reasoning")
            or ""
        ),

        "guardrail_allowed": result.get(
            "guardrail_allowed",
            True,
        ),

        "guardrail_reason": (
            result.get("guardrail_reason")
            or ""
        ),

        "approved": result.get(
            "approved"
        ),

        "human_feedback": (
            result.get("human_feedback")
            or ""
        ),

        "llm_calls": result.get(
            "llm_calls",
            0,
        ),
    }


# =========================================================
# Start Travel Workflow
# =========================================================

async def run_travel_agent(
    user_input: str,
    thread_id: str | None = None,
) -> dict[str, Any]:
    """
    Start a new TripMate LangGraph workflow.

    If a thread_id is supplied, the existing LangGraph
    conversation/checkpoint thread is used.
    """

    if not user_input or not user_input.strip():
        raise ValueError(
            "Travel request cannot be empty."
        )

    # -----------------------------------------------------
    # Create thread ID
    # -----------------------------------------------------

    if thread_id is None:
        thread_id = (
            f"user_{uuid.uuid4().hex}"
        )

    # -----------------------------------------------------
    # LangGraph configuration
    # -----------------------------------------------------

    config = {
        "configurable": {
            "thread_id": thread_id,
        }
    }

    # -----------------------------------------------------
    # Initial State
    # -----------------------------------------------------

    initial_state = {
        "messages": [
            HumanMessage(
                content=user_input.strip()
            )
        ],

        "user_query": user_input.strip(),

        "guardrail_allowed": True,

        "guardrail_reason": "",

        "selected_agents": [],

        "trip_constraints": (
            EMPTY_CONSTRAINTS.copy()
        ),

        "supervisor_reasoning": "",

        "flight_results": "",

        "hotel_results": "",

        "weather_results": "",

        "budget_results": "",

        "itinerary": "",

        "approval_request": "",

        "approved": False,

        "human_feedback": "",

        "final_response": "",

        "llm_calls": 0,
    }

    # -----------------------------------------------------
    # Execute LangGraph
    # -----------------------------------------------------

    result = await travel_graph.ainvoke(
        initial_state,
        config=config,
    )

    # -----------------------------------------------------
    # Serialize result
    # -----------------------------------------------------

    return _serialize_result(
        result,
        thread_id,
    )


# =========================================================
# Resume Human Approval
# =========================================================

async def resume_travel_agent(
    thread_id: str,
    approved: bool,
    feedback: str = "",
) -> dict[str, Any]:
    """
    Resume a paused LangGraph workflow after human approval.

    The original workflow state is recovered from the
    PostgreSQL LangGraph checkpointer using thread_id.
    """

    if not thread_id:
        raise ValueError(
            "thread_id is required to resume the workflow."
        )

    # -----------------------------------------------------
    # LangGraph configuration
    # -----------------------------------------------------

    config = {
        "configurable": {
            "thread_id": thread_id,
        }
    }

    # -----------------------------------------------------
    # Resume interrupted workflow
    # -----------------------------------------------------

    result = await travel_graph.ainvoke(
        Command(
            resume={
                "approved": bool(approved),
                "feedback": (
                    feedback.strip()
                    if feedback
                    else ""
                ),
            }
        ),
        config=config,
    )

    # -----------------------------------------------------
    # Serialize result
    # -----------------------------------------------------

    return _serialize_result(
        result,
        thread_id,
    )