"""
LangGraph PostgreSQL checkpointer for TripMate AI.

The PostgreSQL checkpointer provides persistent LangGraph
state across application restarts.
"""

from __future__ import annotations

from langgraph.checkpoint.postgres import PostgresSaver

from app.core.logging import get_logger
from app.database.postgres import create_connection


logger = get_logger(__name__)


# ---------------------------------------------------------
# Create Checkpointer
# ---------------------------------------------------------

def get_checkpointer() -> PostgresSaver:
    """
    Create and initialize the LangGraph PostgreSQL
    checkpointer.
    """

    connection = create_connection()

    try:
        checkpointer = PostgresSaver(connection)

        # Create LangGraph checkpoint tables
        checkpointer.setup()

        logger.info(
            "LangGraph PostgreSQL checkpointer initialized."
        )

        return checkpointer

    except Exception:
        # Close connection if initialization fails
        try:
            connection.close()
        except Exception:
            pass

        logger.exception(
            "Failed to initialize LangGraph PostgreSQL "
            "checkpointer."
        )

        raise


# ---------------------------------------------------------
# Global Checkpointer
# ---------------------------------------------------------

checkpointer = get_checkpointer()












# """
# LangGraph PostgreSQL checkpointer.
# """

# from __future__ import annotations

# from langgraph.checkpoint.memory import MemorySaver
# from langgraph.checkpoint.postgres import PostgresSaver

# from app.core.logging import get_logger
# from app.database.postgres import create_connection


# logger = get_logger(__name__)


# def get_checkpointer():
#     """
#     Create the LangGraph PostgreSQL checkpointer.

#     Falls back to MemorySaver if PostgreSQL is unavailable.
#     """

#     try:
#         conn = create_connection()

#         saver = PostgresSaver(conn)

#         # Create LangGraph checkpoint tables.
#         saver.setup()

#         logger.info(
#             "LangGraph PostgreSQL checkpointer initialized."
#         )

#         return saver

#     except Exception as exc:
#         logger.exception(
#             "PostgreSQL checkpointer initialization failed."
#         )

#         logger.warning(
#             "Falling back to MemorySaver."
#         )

#         return MemorySaver()


# # ---------------------------------------------------------
# # Global checkpointer used by LangGraph
# # ---------------------------------------------------------

# checkpointer = get_checkpointer()


# """
# LangGraph PostgreSQL checkpointer for TripMate AI.
# """

# from __future__ import annotations

# from langgraph.checkpoint.postgres import PostgresSaver

# from app.core.logging import get_logger
# from app.database.postgres import create_connection

# logger = get_logger(__name__)


# def get_checkpointer() -> PostgresSaver:
#     """
#     Create and initialize the LangGraph PostgreSQL checkpointer.
#     """

#     connection = create_connection()

#     try:
#         checkpointer = PostgresSaver(connection)

#         # Creates LangGraph checkpoint tables
#         checkpointer.setup()

#         logger.info(
#             "LangGraph PostgreSQL checkpointer initialized successfully."
#         )

#         return checkpointer

#     except Exception:
#         try:
#             connection.close()
#         except Exception:
#             pass

#         logger.exception(
#             "Failed to initialize LangGraph PostgreSQL checkpointer."
#         )

#         raise


# # =========================================================
# # Global Checkpointer
# # =========================================================

# checkpointer = get_checkpointer()