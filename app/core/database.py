"""
TripMate AI Database Configuration.

Supports:
- PostgreSQL for Render/production
- SQLite for local development
"""

from __future__ import annotations

import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker


# =========================================================
# Configuration
# =========================================================

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./tripmate.db",
)

TRIPMATE_SCHEMA = os.getenv(
    "TRIPMATE_DB_SCHEMA",
    "tripmate",
)


# =========================================================
# Normalize PostgreSQL URL
# =========================================================

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgres://",
        "postgresql+psycopg://",
        1,
    )

elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgresql://",
        "postgresql+psycopg://",
        1,
    )


# =========================================================
# SQLAlchemy Configuration
# =========================================================

if DATABASE_URL.startswith("sqlite"):
    connect_args = {
        "check_same_thread": False,
    }
else:
    connect_args = {
        "options": f"-c search_path={TRIPMATE_SCHEMA},public",
    }


engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
)


# =========================================================
# Session
# =========================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# =========================================================
# Declarative Base
# =========================================================

Base = declarative_base()


# =========================================================
# Database Initialization
# =========================================================

def initialize_database() -> None:
    """
    Initialize the TripMate database.

    PostgreSQL:
        Creates the TripMate schema and application tables.

    SQLite:
        Creates the local SQLite tables.
    """

    if not DATABASE_URL.startswith("sqlite"):
        with engine.begin() as connection:
            connection.execute(
                text(
                    f'CREATE SCHEMA IF NOT EXISTS "{TRIPMATE_SCHEMA}"'
                )
            )

    Base.metadata.create_all(bind=engine)


# =========================================================
# FastAPI Database Dependency
# =========================================================

def get_db():
    """
    FastAPI dependency that provides a database session.
    """

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()