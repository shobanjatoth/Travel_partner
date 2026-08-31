"""
PostgreSQL connection utilities for TripMate AI.

Used by:
- LangGraph PostgreSQL checkpointer
- PostgreSQL-specific operations
"""

from __future__ import annotations

import psycopg
from psycopg.rows import dict_row

from app.core.config import settings
from app.core.exceptions import DatabaseConnectionError
from app.core.logging import get_logger


logger = get_logger(__name__)


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

TRIPMATE_SCHEMA = getattr(
    settings,
    "TRIPMATE_DB_SCHEMA",
    "tripmate",
)


# ---------------------------------------------------------
# Database URL
# ---------------------------------------------------------

def get_database_url() -> str:
    """
    Return a normalized PostgreSQL connection URL.

    Render PostgreSQL requires SSL, so sslmode=require
    is automatically added when not already present.
    """

    database_url = settings.DATABASE_URL

    if not database_url:
        raise DatabaseConnectionError(
            "DATABASE_URL is missing."
        )

    # Normalize old postgres:// URLs
    if database_url.startswith("postgres://"):
        database_url = database_url.replace(
            "postgres://",
            "postgresql://",
            1,
        )

    # Add SSL for Render PostgreSQL
    if "sslmode=" not in database_url:
        separator = (
            "&"
            if "?" in database_url
            else "?"
        )

        database_url = (
            f"{database_url}"
            f"{separator}"
            f"sslmode=require"
        )

    return database_url


# ---------------------------------------------------------
# PostgreSQL Connection
# ---------------------------------------------------------

def create_connection() -> psycopg.Connection:
    """
    Create a PostgreSQL connection dedicated to TripMate.

    The connection:
    - Uses Render PostgreSQL
    - Enables SSL
    - Creates the TripMate schema
    - Sets TripMate schema as the search path
    """

    try:
        connection = psycopg.connect(
            conninfo=get_database_url(),
            autocommit=True,
            row_factory=dict_row,
        )

        # Create dedicated TripMate schema
        connection.execute(
            f'CREATE SCHEMA IF NOT EXISTS "{TRIPMATE_SCHEMA}"'
        )

        # Use TripMate schema first
        connection.execute(
            f'SET search_path TO "{TRIPMATE_SCHEMA}", public'
        )

        logger.info(
            "Connected to PostgreSQL successfully. "
            "Schema=%s",
            TRIPMATE_SCHEMA,
        )

        return connection

    except Exception as exc:
        logger.exception(
            "Failed to connect to PostgreSQL."
        )

        raise DatabaseConnectionError(
            f"PostgreSQL connection failed: {exc}"
        ) from exc













# """
# PostgreSQL connection utilities for TripMate.
# """

# from __future__ import annotations

# import psycopg
# from psycopg.rows import dict_row

# from app.core.config import settings
# from app.core.exceptions import DatabaseConnectionError
# from app.core.logging import get_logger


# logger = get_logger(__name__)

# TRIPMATE_SCHEMA = "tripmate"


# def get_database_url() -> str:
#     """
#     Return PostgreSQL connection URL.
#     """

#     database_url = settings.DATABASE_URL

#     if not database_url:
#         raise DatabaseConnectionError(
#             "DATABASE_URL is missing."
#         )

#     # Normalize Render PostgreSQL URLs.
#     if database_url.startswith("postgres://"):
#         database_url = database_url.replace(
#             "postgres://",
#             "postgresql://",
#             1,
#         )

#     # psycopg connection
#     if "sslmode=" not in database_url:
#         separator = "&" if "?" in database_url else "?"
#         database_url = (
#             f"{database_url}"
#             f"{separator}sslmode=require"
#         )

#     return database_url


# def create_connection() -> psycopg.Connection:
#     """
#     Create a PostgreSQL connection dedicated to TripMate.
#     """

#     try:
#         connection = psycopg.connect(
#             conninfo=get_database_url(),
#             autocommit=True,
#             row_factory=dict_row,
#         )

#         # Create TripMate schema if necessary.
#         connection.execute(
#             f'CREATE SCHEMA IF NOT EXISTS "{TRIPMATE_SCHEMA}"'
#         )

#         # Make TripMate schema the first search path.
#         connection.execute(
#             f'SET search_path TO "{TRIPMATE_SCHEMA}", public'
#         )

#         logger.info(
#             "Connected to PostgreSQL using schema: %s",
#             TRIPMATE_SCHEMA,
#         )

#         return connection

#     except Exception as exc:
#         logger.exception(
#             "Failed to connect to PostgreSQL."
#         )

#         raise DatabaseConnectionError(
#             str(exc)
#         ) from exc








# """
# PostgreSQL connection utilities for TripMate AI.
# """

# from __future__ import annotations

# import psycopg
# from psycopg.rows import dict_row

# from app.core.config import settings
# from app.core.exceptions import DatabaseConnectionError
# from app.core.logging import get_logger


# logger = get_logger(__name__)

# TRIPMATE_SCHEMA = getattr(
#     settings,
#     "TRIPMATE_DB_SCHEMA",
#     "tripmate",
# )


# def get_database_url() -> str:
#     """
#     Return a normalized PostgreSQL connection URL.
#     """

#     database_url = settings.DATABASE_URL

#     if not database_url:
#         raise DatabaseConnectionError(
#             "DATABASE_URL is missing."
#         )

#     if database_url.startswith("postgres://"):
#         database_url = database_url.replace(
#             "postgres://",
#             "postgresql://",
#             1,
#         )

#     if "sslmode=" not in database_url:
#         separator = "&" if "?" in database_url else "?"
#         database_url = (
#             f"{database_url}"
#             f"{separator}sslmode=require"
#         )

#     return database_url


# def create_connection() -> psycopg.Connection:
#     """
#     Create a PostgreSQL connection for TripMate.

#     TripMate uses its own PostgreSQL schema so it can share
#     the same Render PostgreSQL database with another project.
#     """

#     try:
#         connection = psycopg.connect(
#             conninfo=get_database_url(),
#             autocommit=True,
#             row_factory=dict_row,
#         )

#         connection.execute(
#             f'CREATE SCHEMA IF NOT EXISTS "{TRIPMATE_SCHEMA}"'
#         )

#         connection.execute(
#             f'SET search_path TO "{TRIPMATE_SCHEMA}", public'
#         )

#         logger.info(
#             "Connected to PostgreSQL. Schema=%s",
#             TRIPMATE_SCHEMA,
#         )

#         return connection

#     except Exception as exc:
#         logger.exception(
#             "Failed to connect to PostgreSQL."
#         )

#         raise DatabaseConnectionError(
#             f"PostgreSQL connection failed: {exc}"
#         ) from exc