# """
# Travel API Routes
# """

# from __future__ import annotations

# from fastapi import APIRouter, HTTPException, status

# from app.api.dependencies import validate_feedback
# from app.api.schemas import ApprovalRequest, TravelAgentResponse, TravelRequest
# from app.core.logging import get_logger
# from app.services.travel_service import resume_travel_agent, run_travel_agent

# logger = get_logger(__name__)

# router = APIRouter(
#     prefix="/travel",
#     tags=["Travel Planner Agent"],
# )


# @router.post(
#     "",
#     response_model=TravelAgentResponse,
#     status_code=status.HTTP_200_OK,
#     summary="Create or Continue Travel Plan",
#     description="Initiates the multi-agent travel execution workflow (Guardrail ➔ Supervisor ➔ Domain Specialist Agents).",
# )
# async def create_trip(request: TravelRequest):
#     """
#     Start a new travel planning agent run.
#     """
#     try:
#         result = await run_travel_agent(
#             user_input=request.message,
#             thread_id=request.thread_id,
#         )
#         return result
#     except Exception as exc:
#         logger.exception("Travel request failed.")
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=str(exc),
#         ) from exc


# @router.post(
#     "/approve",
#     response_model=TravelAgentResponse,
#     status_code=status.HTTP_200_OK,
#     summary="Approve or Reject Itinerary (Human-In-The-Loop)",
#     description="Resumes a paused LangGraph workflow with user approval or revision instructions.",
# )
# async def approve_trip(request: ApprovalRequest):
#     """
#     Approve or reject a generated itinerary (Human-in-the-Loop).
#     """
#     validate_feedback(
#         request.approved,
#         request.feedback,
#     )

#     try:
#         result = await resume_travel_agent(
#             thread_id=request.thread_id,
#             approved=request.approved,
#             feedback=request.feedback,
#         )
#         return result
#     except Exception as exc:
#         logger.exception("Approval failed.")
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=str(exc),
#         ) from exc










# """
# Travel Planner API Routes - Integrated with travel_service.py and JWT Authentication
# """

# from __future__ import annotations

# import uuid
# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session

# from app.api.schemas import ApprovalRequest, TravelAgentResponse, TravelRequest
# from app.core.database import get_db
# from app.core.security import get_current_user_email
# from app.db.models import TravelSession, User
# from app.services.travel_service import resume_travel_agent, run_travel_agent

# router = APIRouter(
#     prefix="/travel",
#     tags=["Travel Planner Agent"],
# )


# def validate_feedback(approved: bool, feedback: str) -> None:
#     """Ensure feedback is supplied when an itinerary is rejected."""
#     if not approved and not feedback.strip():
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Feedback is required when requesting revisions to the itinerary.",
#         )


# @router.post(
#     "",
#     response_model=TravelAgentResponse,
#     status_code=status.HTTP_200_OK,
#     summary="Start or Continue Travel Agent Planning",
# )
# async def plan_trip(
#     request: TravelRequest,
#     current_user_email: str = Depends(get_current_user_email),
#     db: Session = Depends(get_db),
# ):
#     """
#     Triggers the LangGraph multi-agent loop to generate or refine a travel itinerary.
#     """
#     user = db.query(User).filter(User.email == current_user_email).first()
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="User identity not found in database.",
#         )

#     # Construct user-isolated session thread ID if none provided
#     thread_id = request.thread_id or f"user_{user.id}_session_{uuid.uuid4().hex[:8]}"

#     try:
#         # Invoke LangGraph travel service workflow
#         service_response = await run_travel_agent(
#             user_input=request.message,
#             thread_id=thread_id,
#         )

#         # Store or update session checkpoint in DB
#         session_rec = (
#             db.query(TravelSession)
#             .filter(TravelSession.thread_id == thread_id)
#             .first()
#         )
#         if not session_rec:
#             session_rec = TravelSession(
#                 user_id=user.id,
#                 thread_id=thread_id,
#                 last_prompt=request.message,
#                 last_response=service_response.get("answer", ""),
#             )
#             db.add(session_rec)
#         else:
#             session_rec.last_prompt = request.message
#             session_rec.last_response = service_response.get("answer", "")

#         db.commit()

#         return TravelAgentResponse(**service_response)

#     except Exception as exc:
#         db.rollback()
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"LangGraph execution error: {str(exc)}",
#         ) from exc


# @router.post(
#     "/approve",
#     response_model=TravelAgentResponse,
#     status_code=status.HTTP_200_OK,
#     summary="Approve or Request Revision for Generated Itinerary",
# )
# async def approve_trip(
#     request: ApprovalRequest,
#     current_user_email: str = Depends(get_current_user_email),
#     db: Session = Depends(get_db),
# ):
#     """
#     Resumes an interrupted travel workflow (Human-in-the-Loop) using LangGraph Commands.
#     """
#     validate_feedback(request.approved, request.feedback)

#     # Verify session belongs to authenticated user
#     user = db.query(User).filter(User.email == current_user_email).first()
#     session_rec = (
#         db.query(TravelSession)
#         .filter(
#             TravelSession.thread_id == request.thread_id,
#             TravelSession.user_id == user.id,
#         )
#         .first()
#     )

#     if not session_rec:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Session thread not found or access denied.",
#         )

#     try:
#         # Resume interrupted LangGraph execution
#         service_response = await resume_travel_agent(
#             thread_id=request.thread_id,
#             approved=request.approved,
#             feedback=request.feedback,
#         )

#         # Update database session record
#         session_rec.last_response = service_response.get("answer", "")
#         db.commit()

#         return TravelAgentResponse(**service_response)

#     except Exception as exc:
#         db.rollback()
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Failed to process approval workflow: {str(exc)}",
#         ) from exc













# """
# Travel API Routes
# """

# from __future__ import annotations

# from fastapi import APIRouter, HTTPException

# from app.api.dependencies import validate_feedback
# from app.api.schemas import ApprovalRequest, TravelRequest
# from app.core.logging import get_logger
# from app.services.travel_service import resume_travel_agent, run_travel_agent

# logger = get_logger(__name__)

# router = APIRouter(
#     prefix="/travel",
#     tags=["Travel"],
# )


# @router.post("")
# async def create_trip(request: TravelRequest):
#     """
#     Start a new travel planning agent run.
#     """
#     try:
#         return await run_travel_agent(
#             user_input=request.message,
#             thread_id=request.thread_id,
#         )
#     except Exception as exc:
#         logger.exception("Travel request failed.")
#         raise HTTPException(
#             status_code=500,
#             detail=str(exc),
#         ) from exc


# @router.post("/approve")
# async def approve_trip(request: ApprovalRequest):
#     """
#     Approve or reject a generated itinerary (Human-in-the-Loop).
#     """
#     validate_feedback(
#         request.approved,
#         request.feedback,
#     )

#     try:
#         return await resume_travel_agent(
#             thread_id=request.thread_id,
#             approved=request.approved,
#             feedback=request.feedback,
#         )
#     except Exception as exc:
#         logger.exception("Approval failed.")
#         raise HTTPException(
#             status_code=500,
#             detail=str(exc),
#         ) from exc



"""
Travel Planner API Routes - Integrated with travel_service.py and JWT Authentication
"""

from __future__ import annotations

import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.schemas import ApprovalRequest, TravelAgentResponse, TravelRequest
from app.core.database import get_db
from app.core.security import get_current_user_email
from app.db.models import TravelSession, User
from app.services.travel_service import resume_travel_agent, run_travel_agent

router = APIRouter(
    prefix="/travel",
    tags=["Travel Planner Agent"],
)


def validate_feedback(approved: bool, feedback: str) -> None:
    """Ensure feedback is supplied when an itinerary is rejected."""
    if not approved and not feedback.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Feedback is required when requesting revisions to the itinerary.",
        )


@router.post(
    "",
    response_model=TravelAgentResponse,
    status_code=status.HTTP_200_OK,
    summary="Start or Continue Travel Agent Planning",
)
async def plan_trip(
    request: TravelRequest,
    current_user_email: str = Depends(get_current_user_email),
    db: Session = Depends(get_db),
):
    """
    Triggers the LangGraph multi-agent loop to generate or refine a travel itinerary.
    """
    user = db.query(User).filter(User.email == current_user_email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User identity not found in database.",
        )

    # Construct user-isolated session thread ID if none provided
    thread_id = request.thread_id or f"user_{user.id}_session_{uuid.uuid4().hex[:8]}"

    try:
        # Invoke LangGraph travel service workflow
        service_response = await run_travel_agent(
            user_input=request.message,
            thread_id=thread_id,
        )

        # Store or update session checkpoint in DB
        session_rec = (
            db.query(TravelSession)
            .filter(TravelSession.thread_id == thread_id)
            .first()
        )
        if not session_rec:
            session_rec = TravelSession(
                user_id=user.id,
                thread_id=thread_id,
                last_prompt=request.message,
                last_response=service_response.get("answer", ""),
            )
            db.add(session_rec)
        else:
            session_rec.last_prompt = request.message
            session_rec.last_response = service_response.get("answer", "")

        db.commit()

        return TravelAgentResponse(**service_response)

    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"LangGraph execution error: {str(exc)}",
        ) from exc


@router.post(
    "/approve",
    response_model=TravelAgentResponse,
    status_code=status.HTTP_200_OK,
    summary="Approve or Request Revision for Generated Itinerary",
)
async def approve_trip(
    request: ApprovalRequest,
    current_user_email: str = Depends(get_current_user_email),
    db: Session = Depends(get_db),
):
    """
    Resumes an interrupted travel workflow (Human-in-the-Loop) using LangGraph Commands.
    """
    validate_feedback(request.approved, request.feedback)

    # Verify session belongs to authenticated user
    user = db.query(User).filter(User.email == current_user_email).first()
    session_rec = (
        db.query(TravelSession)
        .filter(
            TravelSession.thread_id == request.thread_id,
            TravelSession.user_id == user.id,
        )
        .first()
    )

    if not session_rec:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session thread not found or access denied.",
        )

    try:
        # Resume interrupted LangGraph execution
        service_response = await resume_travel_agent(
            thread_id=request.thread_id,
            approved=request.approved,
            feedback=request.feedback,
        )

        # Update database session record
        session_rec.last_response = service_response.get("answer", "")
        db.commit()

        return TravelAgentResponse(**service_response)

    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process approval workflow: {str(exc)}",
        ) from exc