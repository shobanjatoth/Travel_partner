# """
# TripMate AI - Application Entry Point
# """

# from __future__ import annotations

# from contextlib import asynccontextmanager
# from pathlib import Path

# import nest_asyncio
# import uvicorn
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import FileResponse, JSONResponse
# from fastapi.staticfiles import StaticFiles

# # Import DB and Routers
# from app.api.auth_routes import router as auth_router
# from app.api.routes import router as travel_router
# from app.api.schemas import HealthResponse
# from app.core.config import settings
# from app.core.database import Base, engine
# from app.core.logging import get_logger

# # Apply nest_asyncio for nested event loop support
# nest_asyncio.apply()

# logger = get_logger(__name__)

# BASE_DIR = Path(__file__).resolve().parent.parent
# FRONTEND_DIR = BASE_DIR / "frontend"


# # ---------------------------------------------------------
# # Lifespan Context Manager & DB Setup
# # ---------------------------------------------------------

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     logger.info("=" * 60)
#     logger.info("%s starting...", settings.APP_NAME)
#     logger.info("Environment : %s", settings.ENVIRONMENT)
#     logger.info("Debug       : %s", settings.DEBUG)
#     logger.info("=" * 60)

#     # Automatically create database tables if they don't exist
#     Base.metadata.create_all(bind=engine)
#     logger.info("Database tables initialized successfully.")

#     yield

#     logger.info("%s stopped.", settings.APP_NAME)


# # ---------------------------------------------------------
# # FastAPI App Instance Configuration
# # ---------------------------------------------------------

# app = FastAPI(
#     title=f"{settings.APP_NAME} API",
#     version="1.0.0",
#     debug=settings.DEBUG,
#     lifespan=lifespan,
#     docs_url="/docs",
#     redoc_url="/redoc",
#     description=(
#         "Production-ready AI Travel Planner built using "
#         "LangGraph, LangChain, Groq, PostgreSQL, and FastAPI.\n\n"
#         "### Features:\n"
#         "- **JWT Authentication**: Secure user registration & session handling\n"
#         "- **Multi-Agent Orchestration**: Supervisor and domain agent workflows\n"
#         "- **Human-in-the-Loop**: Approval checkpoint before finalizing travel plans\n"
#     ),
# )

# # Enable CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ---------------------------------------------------------
# # Static Files & Frontend Configuration
# # ---------------------------------------------------------

# if FRONTEND_DIR.exists():
#     css_dir = FRONTEND_DIR / "css"
#     js_dir = FRONTEND_DIR / "js"
#     pages_dir = FRONTEND_DIR / "pages"

#     if css_dir.exists():
#         app.mount("/css", StaticFiles(directory=css_dir), name="css")
#     if js_dir.exists():
#         app.mount("/js", StaticFiles(directory=js_dir), name="js")
#     if pages_dir.exists():
#         app.mount("/pages", StaticFiles(directory=pages_dir), name="pages")

# # Legacy /static fallback
# static_dir = BASE_DIR / "static"
# if static_dir.exists():
#     app.mount("/static", StaticFiles(directory=static_dir), name="static")

# # ---------------------------------------------------------
# # API Router Registrations
# # ---------------------------------------------------------

# app.include_router(auth_router, prefix="/api")
# app.include_router(travel_router, prefix="/api")


# # ---------------------------------------------------------
# # Page & Health Check Handlers
# # ---------------------------------------------------------

# @app.get("/", response_class=FileResponse, include_in_schema=False)
# async def home():
#     """Serves the main protected dashboard HTML page."""
#     dashboard_path = FRONTEND_DIR / "pages" / "dashboard.html"
#     if dashboard_path.exists():
#         return FileResponse(dashboard_path)
#     return FileResponse(BASE_DIR / "templates" / "index.html")


# @app.get("/login", response_class=FileResponse, include_in_schema=False)
# async def login_page():
#     """Serves the authentication (Login/Signup) HTML page."""
#     login_path = FRONTEND_DIR / "pages" / "login.html"
#     if login_path.exists():
#         return FileResponse(login_path)
#     return FileResponse(BASE_DIR / "templates" / "login.html")


# @app.get(
#     "/health",
#     response_model=HealthResponse,
#     tags=["Health Check"],
#     summary="System Health Check",
#     description="Returns current system operating status and version.",
# )
# async def health():
#     return HealthResponse(
#         status="ok",
#         message=f"{settings.APP_NAME} is running",
#         version="1.0.0",
#     )


# @app.get("/favicon.ico", include_in_schema=False)
# async def favicon():
#     return JSONResponse(content={})


# # ---------------------------------------------------------
# # Local Execution Entry
# # ---------------------------------------------------------

# if __name__ == "__main__":
#     uvicorn.run(
#         "app.main:app",
#         host=getattr(settings, "HOST", "0.0.0.0"),
#         port=getattr(settings, "PORT", 8000),
#         reload=settings.DEBUG,
#     ) 
    









"""
TripMate AI - Application Entry Point
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path

import nest_asyncio
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.api.auth_routes import router as auth_router
from app.api.routes import router as travel_router
from app.api.schemas import HealthResponse
from app.core.config import settings
from app.core.database import initialize_database
from app.core.logging import get_logger


# ---------------------------------------------------------
# Event Loop Support
# ---------------------------------------------------------

nest_asyncio.apply()

logger = get_logger(__name__)


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"


# ---------------------------------------------------------
# Application Lifespan
# ---------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown lifecycle.
    """

    logger.info("=" * 60)
    logger.info("%s starting...", settings.APP_NAME)
    logger.info("Environment : %s", settings.ENVIRONMENT)
    logger.info("Debug       : %s", settings.DEBUG)
    logger.info("=" * 60)

    # -----------------------------------------------------
    # Initialize Application Database
    # -----------------------------------------------------

    try:
        initialize_database()

        logger.info(
            "Application database initialized successfully."
        )

    except Exception:
        logger.exception(
            "Application database initialization failed."
        )
        raise

    yield

    logger.info(
        "%s stopped.",
        settings.APP_NAME,
    )


# ---------------------------------------------------------
# FastAPI Application
# ---------------------------------------------------------

app = FastAPI(
    title=f"{settings.APP_NAME} API",
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    description=(
        "Production-ready AI Travel Planner built using "
        "LangGraph, LangChain, Groq, PostgreSQL, and FastAPI."
        "\n\n"
        "### Features:"
        "\n"
        "- **JWT Authentication**: Secure user registration "
        "& session handling"
        "\n"
        "- **Multi-Agent Orchestration**: Supervisor and "
        "domain agent workflows"
        "\n"
        "- **Human-in-the-Loop**: Approval checkpoint before "
        "finalizing travel plans"
    ),
)


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# Frontend Static Files
# ---------------------------------------------------------

if FRONTEND_DIR.exists():

    css_dir = FRONTEND_DIR / "css"
    js_dir = FRONTEND_DIR / "js"
    pages_dir = FRONTEND_DIR / "pages"

    if css_dir.exists():
        app.mount(
            "/css",
            StaticFiles(directory=css_dir),
            name="css",
        )

    if js_dir.exists():
        app.mount(
            "/js",
            StaticFiles(directory=js_dir),
            name="js",
        )

    if pages_dir.exists():
        app.mount(
            "/pages",
            StaticFiles(directory=pages_dir),
            name="pages",
        )


# ---------------------------------------------------------
# Legacy Static Directory
# ---------------------------------------------------------

static_dir = BASE_DIR / "static"

if static_dir.exists():
    app.mount(
        "/static",
        StaticFiles(directory=static_dir),
        name="static",
    )


# ---------------------------------------------------------
# API Routers
# ---------------------------------------------------------

app.include_router(
    auth_router,
    prefix="/api",
)

app.include_router(
    travel_router,
    prefix="/api",
)


# ---------------------------------------------------------
# Home Page
# ---------------------------------------------------------

@app.get(
    "/",
    response_class=FileResponse,
    include_in_schema=False,
)
async def home():
    """
    Serve the main dashboard.
    """

    dashboard_path = (
        FRONTEND_DIR
        / "pages"
        / "dashboard.html"
    )

    if dashboard_path.exists():
        return FileResponse(dashboard_path)

    index_path = (
        BASE_DIR
        / "templates"
        / "index.html"
    )

    if index_path.exists():
        return FileResponse(index_path)

    return JSONResponse(
        content={
            "message": f"{settings.APP_NAME} API is running."
        }
    )


# ---------------------------------------------------------
# Login Page
# ---------------------------------------------------------

@app.get(
    "/login",
    response_class=FileResponse,
    include_in_schema=False,
)
async def login_page():
    """
    Serve the login page.
    """

    login_path = (
        FRONTEND_DIR
        / "pages"
        / "login.html"
    )

    if login_path.exists():
        return FileResponse(login_path)

    template_path = (
        BASE_DIR
        / "templates"
        / "login.html"
    )

    if template_path.exists():
        return FileResponse(template_path)

    return JSONResponse(
        content={
            "message": "Login page not found."
        },
        status_code=404,
    )


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------

@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["Health Check"],
    summary="System Health Check",
)
async def health():
    """
    Return application health status.
    """

    return HealthResponse(
        status="ok",
        message=f"{settings.APP_NAME} is running",
        version=settings.APP_VERSION,
    )


# ---------------------------------------------------------
# Favicon
# ---------------------------------------------------------

@app.get(
    "/favicon.ico",
    include_in_schema=False,
)
async def favicon():
    return JSONResponse(content={})


# ---------------------------------------------------------
# Local Execution
# ---------------------------------------------------------

if __name__ == "__main__":

    uvicorn.run(
        "app.main:app",
        host=getattr(
            settings,
            "HOST",
            "0.0.0.0",
        ),
        port=getattr(
            settings,
            "PORT",
            8000,
        ),
        reload=settings.DEBUG,
    )
    
 