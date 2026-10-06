# ✈️ TripMate AI — A Multi-Agent Travel Planner with MCP

An open-source AI travel planner that turns a natural-language trip request into a practical travel plan with flight suggestions, hotel ideas, weather details, and a day-by-day itinerary. The project uses a multi-agent workflow built with LangGraph, LangChain, FastAPI, and MCP tooling.

## Why this project?

Planning a trip usually means jumping between multiple websites, tools, and spreadsheets. This project brings that flow into one experience by combining:

- a flight-search agent,
- a hotel-research agent,
- a weather agent,
- an itinerary-planning agent, and
- a final response agent,

all coordinated through a LangGraph workflow with MCP-based tool integrations.

## Features

- ✈️ Flight research using AviationStack
- 🏨 Hotel suggestions using Tavily search
- 🌤 Weather lookup via a custom MCP tool
- 🧠 Multi-agent orchestration with LangGraph and MCP
- 📝 Structured travel itinerary generation
- 🌐 FastAPI backend with a simple web interface
- 💾 Conversation state persistence using PostgreSQL
- ⚡ LLM-powered responses with Groq

## Tech Stack

- Python 3.10+
- FastAPI
- Jinja2 + HTML/CSS/JavaScript frontend
- LangGraph
- LangChain
- Groq LLMs
- PostgreSQL
- Tavily API
- AviationStack API
- MCP via `langchain-mcp-adapters` and `mcp`

## State and MCP Integration

This project integrates MCP in several places:

- `Tavily` search uses a remote MCP endpoint at `https://mcp.tavily.com/mcp/`
- `AviationStack` uses a local stdio MCP command: `uvx aviationstack-mcp`
- `Weather` is implemented with a custom local MCP server in `custom_weather_mcp_server.py`

The MCP client is defined in `mcp_client.py`, which exposes async helper functions for:

- `tavily_mcp_search`
- `aviation_mcp_call`
- `weather_mcp_search`
- `forecast_mcp_search`
- `extract_destination`

The main travel workflow in `backend.py` calls these helpers from the flight, hotel, and weather agents.

## Project Structure

```text
TripMate/
│
├── .github/
│   └── workflows/
│       ├── ci.yml                  # CI pipeline: testing and validation
│       └── deploy.yml              # Deployment workflow
│
├── app/
│   ├── agents/                     # AI agents and travel planning logic
│   │   ├── __init__.py
│   │   ├── budget.py               # Budget planning agent
│   │   ├── flight.py               # Flight planning/search agent
│   │   ├── guardrail.py            # Input/output safety validation
│   │   ├── hotel.py                # Hotel planning/search agent
│   │   ├── itinerary.py            # Itinerary generation agent
│   │   ├── responder.py            # Final response generation
│   │   ├── reviewer.py             # Plan review/validation agent
│   │   ├── supervisor.py            # Agent supervisor/orchestrator
│   │   └── weather.py              # Weather-related agent
│   │
│   ├── api/                        # FastAPI routes and API schemas
│   │   ├── __init__.py
│   │   ├── auth_routes.py          # Authentication endpoints
│   │   ├── dependencies.py         # API dependencies
│   │   ├── routes.py               # Main API endpoints
│   │   └── schemas.py              # Request/response schemas
│   │
│   ├── core/                       # Application configuration and utilities
│   │   ├── __init__.py
│   │   ├── config.py               # Environment/configuration settings
│   │   ├── constants.py            # Application constants
│   │   ├── database.py             # Database configuration
│   │   ├── exceptions.py            # Custom exceptions
│   │   ├── logging.py              # Logging configuration
│   │   ├── security.py             # Authentication/security utilities
│   │   └── text_utils.py            # Text processing utilities
│   │
│   ├── database/                   # Database and checkpoint management
│   │   ├── __init__.py
│   │   ├── checkpoint.py            # Graph/checkpoint persistence
│   │   └── postgres.py              # PostgreSQL integration
│   │
│   ├── db/
│   │   └── models.py               # Database models
│   │
│   ├── graph/                      # LangGraph workflow
│   │   ├── __init__.py
│   │   ├── builder.py              # Builds the agent graph
│   │   ├── router.py               # Routes between graph nodes
│   │   └── state.py                # Shared graph state
│   │
│   ├── llm/                        # LLM integration
│   │   ├── __init__.py
│   │   ├── groq_client.py          # Groq LLM client
│   │   ├── parser.py               # LLM output parsing
│   │   └── prompts.py              # System and agent prompts
│   │
│   ├── mcp/                        # MCP server integrations
│   │   └── servers/
│   │       └── weather_server.py   # Weather MCP server
│   │
│   ├── tools/                      # External tools and tool registry
│   │   ├── tavily.py               # Tavily search integration
│   │   ├── weather.py              # Weather tool
│   │   ├── client.py               # Tool client
│   │   └── registry.py             # Tool registration
│   │
│   ├── services/                   # Business/service layer
│   │   ├── __init__.py
│   │   ├── destination_service.py # Destination-related services
│   │   └── travel_service.py      # Travel planning services
│   │
│   ├── __init__.py
│   └── main.py                     # FastAPI application entry point
│
├── frontend/                       # Frontend application
│   ├── css/
│   │   ├── components.css
│   │   └── main.css
│   │
│   ├── js/
│   │   ├── api.js                  # API communication
│   │   ├── auth.js                 # Authentication logic
│   │   ├── config.js               # Frontend configuration
│   │   └── travel.js               # Travel UI logic
│   │
│   └── pages/
│       ├── dashboard.html          # Main dashboard
│       └── login.html              # Login page
│
├── tests/                          # Automated tests
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_budget.py
│   ├── test_flight.py
│   ├── test_graph.py
│   ├── test_guardrail.py
│   ├── test_itinerary.py
│   ├── test_supervisor.py
│   └── test_weather.py
│
├── .gitignore
├── Dockerfile                      # Docker container configuration
├── LICENSE
├── README.md
├── api_test.py                     # API testing script
├── render.yaml                     # Render deployment configuration
├── requirements.txt                # Python dependencies
├── template.py                     # Project/template utility
└── tripmate.db                     # Local SQLite database
```

## Prerequisites

Before running the project locally, make sure you have:

- Python 3.10 or newer installed
- PostgreSQL running and accessible
- API keys for:
  - Groq
  - Tavily
  - AviationStack
  - OpenWeather
- `uvx` available for local `aviationstack-mcp` usage (or adjust `mcp_client.py` accordingly)

## Environment Variables

Create a `.env` file in the project root with the following variables:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/travel_db
GROQ_API_KEY=your_groq_api_key
AVIATIONSTACK_API_KEY=your_aviationstack_api_key
TAVILY_API_KEY=your_tavily_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
DEFAULT_ORIGIN_IATA=DAC
```

## Installation

```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Running the App

Start the FastAPI server:

```bash
python app.py
```

Then open your browser at:

```text
http://127.0.0.1:8000/
```

## Using MCP Tools

The app uses MCP behind the scenes, so there is no separate frontend change required after the environment is set up.

If you need to customize the weather MCP server command, edit `mcp_client.py` and update the `weather` tool path to your local Python environment.

## API Endpoints

- GET /health - Health check
- POST /api/travel - Submit a travel request

Example request:

```bash
curl -X POST http://127.0.0.1:8000/api/travel \
  -H "Content-Type: application/json" \
  -d '{"message":"Plan a 3-day trip to Tokyo with a budget of $1200"}'
```

## How the Workflow Works

1. The user submits a travel request.
2. The flight agent uses MCP-backed AviationStack data.
3. The hotel agent uses a remote Tavily MCP search.
4. The weather agent calls the custom weather MCP server.
5. The itinerary agent creates a practical travel plan.
6. The final response is returned through the web API.

## Contributing

Contributions are welcome. If you want to improve the app, add new travel features, or fix issues:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Open a pull request

## Acknowledgments

This project is built with the help of modern LLM tooling, MCP integrations, and travel APIs. It is intended as a practical example of combining LangGraph agents with real-world applications.
