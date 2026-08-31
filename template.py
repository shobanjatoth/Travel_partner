import os
import logging
from pathlib import Path

# Configure logging to monitor file creation
logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

list_of_files = [
    # GitHub Actions Workflows
    ".github/workflows/ci.yml",
    ".github/workflows/deploy.yml",

    # Core Application Modules
    "app/__init__.py",
    "app/main.py",
    
    # Agents
    "app/agents/__init__.py",
    "app/agents/budget.py",
    "app/agents/flight.py",
    "app/agents/guardrail.py",
    "app/agents/hotel.py",
    "app/agents/itinerary.py",
    "app/agents/responder.py",
    "app/agents/reviewer.py",
    "app/agents/supervisor.py",
    "app/agents/weather.py",

    # API Layer
    "app/api/__init__.py",
    "app/api/dependencies.py",
    "app/api/routes.py",
    "app/api/schemas.py",

    # Core Config & Utils
    "app/core/__init__.py",
    "app/core/config.py",
    "app/core/constants.py",
    "app/core/logging.py",

    # Database
    "app/database/__init__.py",
    "app/database/checkpoint.py",

    # Graph State & Logic
    "app/graph/__init__.py",
    "app/graph/builder.py",
    "app/graph/router.py",
    "app/graph/state.py",

    # LLM Clients & Prompts
    "app/llm/__init__.py",
    "app/llm/groq_client.py",
    "app/llm/prompts.py",

    # Business Services
    "app/services/__init__.py",
    "app/services/destination_service.py",
    "app/services/travel_service.py",

    # Frontend Assets
    "static/css/style.css",
    "static/js/app.js",
    "templates/index.html",

    # Test Suite
    "tests/__init__.py",
    "tests/test_api.py",
    "tests/test_budget.py",
    "tests/test_flight.py",
    "tests/test_graph.py",
    "tests/test_guardrail.py",
    "tests/test_itinerary.py",
    "tests/test_supervisor.py",
    "tests/test_weather.py",

    # Infrastructure & Config Files
    ".env",
    "docker-compose.yml",
    "Dockerfile",
    "README.md",
    "render.yaml",
    "requirements.txt",
]

def create_structure():
    for filepath in list_of_files:
        filepath = Path(filepath)
        filedir, filename = os.path.split(filepath)

        # Create parent directories if they don't exist
        if filedir != "":
            os.makedirs(filedir, exist_ok=True)
            logging.info(f"Creating directory: {filedir} for file: {filename}")

        # Create empty file if it doesn't exist or is empty
        if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
            with open(filepath, "w") as f:
                pass  # create empty file
            logging.info(f"Creating empty file: {filepath}")
        else:
            logging.info(f"File already exists: {filepath}")

if __name__ == "__main__":
    create_structure()