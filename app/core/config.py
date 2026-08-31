# from functools import lru_cache
# from pathlib import Path

# from pydantic import Field
# from pydantic_settings import BaseSettings, SettingsConfigDict

# BASE_DIR = Path(__file__).resolve().parents[2]


# class Settings(BaseSettings):
#     """
#     Centralized application configuration.
#     Values are loaded from the .env file during development
#     and from environment variables in production.
#     """

#     model_config = SettingsConfigDict(
#         env_file=BASE_DIR / ".env",
#         env_file_encoding="utf-8",
#         case_sensitive=True,
#         extra="ignore",
#     )

#     # Application
#     APP_NAME: str = "TripMate AI"
#     APP_VERSION: str = "1.0.0"
#     ENVIRONMENT: str = "development"
#     DEBUG: bool = False
#     HOST: str = "127.0.0.1"
#     PORT: int = 8000

#     # Groq
#     GROQ_API_KEY: str = ""
#     GROQ_MODEL: str = "llama-3.3-70b-versatile"

#     # PostgreSQL
#     DATABASE_URL: str = ""

#     # MCP
#     OPENWEATHER_API_KEY: str = ""
#     AVIATION_STACK_API_KEY: str = ""
#     TAVILY_API_KEY: str = ""

#     # LangSmith
#     LANGCHAIN_TRACING_V2: bool = False
#     LANGCHAIN_API_KEY: str | None = None
#     LANGCHAIN_PROJECT: str = "TripMateAI"

#     # Redis
#     REDIS_URL: str | None = None

#     # Logging
#     LOG_LEVEL: str = "INFO"
#     LOG_FILE: str = "logs/tripmate.log"

#     # Security
#     SECRET_KEY: str = ""
#     JWT_ALGORITHM: str = "HS256"
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60, ge=1)


# @lru_cache
# def get_settings() -> Settings:
#     """
#     Returns a cached Settings instance.
#     The .env file is read only once.
#     """
#     return Settings()


# settings = get_settings()








from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """
    Centralized application configuration.

    Development:
        Values can be loaded from .env.

    Production:
        Values are loaded from environment variables
        configured in Render.
    """

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # ---------------------------------------------------------
    # Application
    # ---------------------------------------------------------

    APP_NAME: str = "TripMate AI"
    APP_VERSION: str = "1.0.0"

    ENVIRONMENT: str = "development"
    DEBUG: bool = False

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # ---------------------------------------------------------
    # Groq
    # ---------------------------------------------------------

    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    # ---------------------------------------------------------
    # PostgreSQL
    # ---------------------------------------------------------
    # PostgreSQL
  
    DATABASE_URL: str = ""

    # Dedicated schema inside the shared PostgreSQL database.
    TRIPMATE_DB_SCHEMA: str = "tripmate"

    # ---------------------------------------------------------
    # MCP / External APIs
    # ---------------------------------------------------------

    OPENWEATHER_API_KEY: str = ""
    AVIATION_STACK_API_KEY: str = ""
    TAVILY_API_KEY: str = ""

    # ---------------------------------------------------------
    # LangSmith
    # ---------------------------------------------------------

    LANGCHAIN_TRACING_V2: bool = False
    LANGCHAIN_API_KEY: str | None = None
    LANGCHAIN_PROJECT: str = "TripMateAI"

    # ---------------------------------------------------------
    # Redis
    # ---------------------------------------------------------

    REDIS_URL: str | None = None

    # ---------------------------------------------------------
    # Logging
    # ---------------------------------------------------------

    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/tripmate.log"

    # ---------------------------------------------------------
    # Security
    # ---------------------------------------------------------

    SECRET_KEY: str = ""

    JWT_ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=60,
        ge=1,
    )


@lru_cache
def get_settings() -> Settings:
    """
    Return a cached Settings instance.
    """

    return Settings()


settings = get_settings()