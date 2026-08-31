"""
Database Models for User Accounts and Travel Sessions
"""

from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    # Relationship to user travel sessions
    sessions = relationship("TravelSession", back_populates="owner", cascade="all, delete-orphan")


class TravelSession(Base):
    __tablename__ = "travel_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    thread_id = Column(String, unique=True, index=True, nullable=False)
    last_prompt = Column(Text, nullable=True)
    last_response = Column(Text, nullable=True)
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationship back to User
    owner = relationship("User", back_populates="sessions")