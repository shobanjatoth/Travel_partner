
# """
# API Request / Response Schemas
# """

# from __future__ import annotations

# from typing import Any, Dict, List, Optional
# from pydantic import BaseModel, Field, ConfigDict


# class TravelRequest(BaseModel):
#     message: str = Field(
#         ...,
#         min_length=1,
#         description="Natural language user travel request",
#         example="Plan a 7-day trip from Hyderabad to Tokyo on a $3000 budget focusing on local food and culture."
#     )
#     thread_id: Optional[str] = Field(
#         default=None,
#         description="Optional LangGraph thread/session ID for resuming conversations",
#         example="thread_abc123"
#     )

#     model_config = ConfigDict(
#         json_schema_extra={
#             "example": {
#                 "message": "Plan a 10-day trip from Hyderabad to New York with budget recommendations.",
#                 "thread_id": "session_8899"
#             }
#         }
#     )


# class ApprovalRequest(BaseModel):
#     thread_id: str = Field(
#         ...,
#         min_length=1,
#         description="LangGraph thread ID associated with the paused workflow state",
#         example="session_8899"
#     )
#     approved: bool = Field(
#         ...,
#         description="Set True to accept the plan, or False to request revisions",
#         example=False
#     )
#     feedback: str = Field(
#         default="",
#         description="Feedback or revision instructions required when approved is False",
#         example="Please change the accommodation to mid-range hotels instead of luxury resorts."
#     )

#     model_config = ConfigDict(
#         json_schema_extra={
#             "example": {
#                 "thread_id": "session_8899",
#                 "approved": False,
#                 "feedback": "Prefer flying with maximum 1 layover and mid-range budget hotels."
#             }
#         }
#     )


# class TravelAgentResponse(BaseModel):
#     thread_id: str = Field(..., description="Unique workflow session identifier")
#     requires_approval: bool = Field(..., description="Indicates if human approval checkpoint was reached")
#     answer: str = Field(..., description="Generated Markdown travel plan or response content")
#     metadata: Optional[Dict[str, Any]] = Field(default={}, description="Agent state execution metadata")

#     model_config = ConfigDict(
#         json_schema_extra={
#             "example": {
#                 "thread_id": "session_8899",
#                 "requires_approval": True,
#                 "answer": "## 📌 Trip Summary\nHere is your proposed itinerary for New York...",
#                 "metadata": {"selected_agents": ["flight_agent", "hotel_agent", "budget_agent"]}
#             }
#         }
#     )


# class HealthResponse(BaseModel):
#     status: str = Field(..., example="ok")
#     message: str = Field(..., example="TripMate AI is running")
#     version: str = Field(..., example="1.0.0")




"""
Pydantic Validation Schemas for Authentication and Travel Endpoints
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ==========================================
# Authentication Schemas
# ==========================================

class UserRegister(BaseModel):
    full_name: str = Field(..., example="John Doe")
    email: EmailStr = Field(..., example="john@example.com")
    password: str = Field(..., min_length=6, example="securepassword123")


class UserLogin(BaseModel):
    email: EmailStr = Field(..., example="john@example.com")
    password: str = Field(..., example="securepassword123")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    email: str
    user_name: str


# ==========================================
# Travel Agent Schemas
# ==========================================

class TravelRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        description="Natural language travel request",
        example="Plan a 5-day trip to Tokyo on a $2500 budget.",
    )
    thread_id: Optional[str] = Field(
        default=None,
        description="Optional session ID for persistent thread memory",
        example="user_1_session_a1b2c3d4",
    )


class ApprovalRequest(BaseModel):
    thread_id: str = Field(..., example="user_1_session_a1b2c3d4")
    approved: bool = Field(..., example=True)
    feedback: str = Field(
        default="",
        example="Change the morning flight to an afternoon departure.",
    )


class TravelAgentResponse(BaseModel):
    thread_id: str
    answer: str
    requires_approval: bool = False
    approval_request: Optional[str] = ""
    flight_results: Optional[str] = ""
    hotel_results: Optional[str] = ""
    weather_results: Optional[str] = ""
    budget_results: Optional[str] = ""
    itinerary: Optional[str] = ""
    selected_agents: List[str] = Field(default_factory=list)
    trip_constraints: Dict[str, Any] = Field(default_factory=dict)
    supervisor_reasoning: Optional[str] = ""
    guardrail_allowed: bool = True
    guardrail_reason: Optional[str] = ""
    approved: Optional[bool] = None
    human_feedback: Optional[str] = ""
    llm_calls: int = 0

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# Health Check Schema
# ==========================================

class HealthResponse(BaseModel):
    status: str
    message: str
    version: str