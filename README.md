# Tripo — Multi-Agent Travel Planner

Tripo is an AI-powered travel planning system that uses a multi-agent
architecture built with LangGraph to generate complete, budget-aware travel
itineraries — including flight information, hotel suggestions, and a
day-by-day plan — from a single natural-language request.

The backend is built with FastAPI and LangGraph, uses PostgreSQL for
conversation state persistence, and exposes a REST API consumed by a
server-rendered web frontend.

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Tech Stack](#tech-stack)
4. [Project Structure](#project-structure)
5. [Prerequisites](#prerequisites)
6. [Installation](#installation)
7. [Configuration](#configuration)
8. [Database Setup](#database-setup)
9. [Running the Application](#running-the-application)
10. [API Reference](#api-reference)
11. [Frontend](#frontend)
12. [Testing](#testing)
13. [Troubleshooting](#troubleshooting)
14. [Roadmap](#roadmap)
15. [Contributing](#contributing)
16. [License](#license)
17. [Author](#author)

---

## Overview

Given a request such as:

> "Plan a complete 7 days Japan trip from Delhi under 5 lakhs."

Tripo processes the request through a sequence of specialized agents and
returns:

- Live flight search results
- Hotel suggestions
- A day-by-day itinerary
- A consolidated, user-facing travel plan

Each conversation is identified by a `thread_id` and checkpointed in
PostgreSQL, allowing a user to continue refining a plan across multiple
requests without losing prior context.

## Architecture

Tripo's core logic is implemented as a directed graph of four agents using
LangGraph's `StateGraph`. Each node updates a shared `TravelState` object,
which is passed to the next node in the pipeline.

```
        START
          │
          ▼
   ┌──────────────┐
   │ Flight Agent │  → live flight search (AviationStack)
   └──────┬───────┘
          ▼
   ┌──────────────┐
   │ Hotel Agent  │  → hotel search (Tavily)
   └──────┬───────┘
          ▼
   ┌────────────────┐
   │ Itinerary Agent│  → day-by-day plan (Groq LLM)
   └──────┬─────────┘
          ▼
   ┌──────────────┐
   │ Final Agent  │  → consolidated response (Groq LLM)
   └──────┬───────┘
          ▼
         END
```

**State object (`TravelState`)**

| Field | Type | Description |
|---|---|---|
| `messages` | `list[AnyMessage]` | Full message history for the thread (accumulated). |
| `user_query` | `str` | The original user request. |
| `flight_results` | `str` | Output of the Flight Agent. |
| `hotel_results` | `str` | Output of the Hotel Agent. |
| `itinerary` | `str` | Output of the Itinerary Agent. |
| `llm_calls` | `int` | Running count of LLM invocations for the request. |

Conversation state is persisted between requests using
`PostgresSaver`, LangGraph's PostgreSQL-backed checkpointer, keyed by
`thread_id`.

## Tech Stack

| Layer | Technology |
|---|---|
| Agent orchestration | LangGraph, LangChain |
| LLM inference | Groq (`llama-3.3-70b-versatile`) |
| Web search / hotel data | Tavily |
| Flight data | AviationStack |
| Backend framework | FastAPI, Uvicorn |
| Database | PostgreSQL (via `psycopg`), hosted on Render |
| Templating | Jinja2 |
| Frontend | HTML, CSS, vanilla JavaScript |
| Markdown rendering (client) | marked.js |
| PDF export (client) | html2pdf.js |
| Observability (optional) | LangSmith |

## Project Structure

```
Tripo-Multi-Agent-Travel-Planner/
├── app.py                  # FastAPI application, routes, request/response models
├── backend.py               # LangGraph graph definition, agents, checkpointer setup
├── test.py                  # Manual CLI test harness for the agent pipeline
├── requirements.txt          # Python dependencies
├── .env.example              # Required environment variables (template)
├── LICENSE                   # MIT License
├── tools/
│   ├── __init__.py
│   ├── flight_tool.py        # AviationStack flight search integration
│   └── tavily_tool.py         # Tavily hotel/web search integration
├── templates/
│   └── index.html             # Main frontend page (Jinja2 template)
└── static/
    ├── style.css               # Frontend styling
    └── script.js                # Frontend behavior (API calls, rendering, UI state)
```

## Prerequisites

- Python 3.10 or later
- A PostgreSQL database (Render is used in this project, but any
  PostgreSQL-compatible instance will work)
- API keys for:
  - [Groq](https://console.groq.com/)
  - [AviationStack](https://aviationstack.com/)
  - [Tavily](https://app.tavily.com/home)
  - [LangSmith](https://smith.langchain.com/) (optional, for tracing)

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Abhay-Chand/Tripo-Multi-Agent-Travel-Planner.git
   cd Tripo-Multi-Agent-Travel-Planner
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS / Linux
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   python -m pip install -r requirements.txt
   ```

## Configuration

Create a `.env` file in the project root, using `.env.example` as a
template:

```env
GROQ_API_KEY="your_groq_key"
AVIATIONSTACK_API_KEY="your_aviationstack_key"
TAVILY_API_KEY="your_tavily_key"

DATABASE_URL="postgresql://username:password@host:5432/database"

LANGSMITH_TRACING="true"
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
LANGSMITH_API_KEY="your_langsmith_key"
LANGSMITH_PROJECT="tripo"
```

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | Yes | Authenticates requests to the Groq LLM API used by the Itinerary and Final agents. |
| `AVIATIONSTACK_API_KEY` | Yes | Used by the Flight Agent for live flight data. |
| `TAVILY_API_KEY` | Yes | Used by the Hotel Agent for web/hotel search. |
| `DATABASE_URL` | Yes | PostgreSQL connection string used for the LangGraph checkpointer. SSL (`sslmode=require`) is enforced automatically if not already present in the URL. |
| `LANGSMITH_TRACING` | No | Enables LangSmith tracing for debugging agent runs. |
| `LANGSMITH_ENDPOINT` | No | LangSmith API endpoint. |
| `LANGSMITH_API_KEY` | No | LangSmith API key. |
| `LANGSMITH_PROJECT` | No | LangSmith project name for grouping traces. |

## Database Setup

1. Sign in to [Render](https://dashboard.render.com/).
2. Select **New** → **PostgreSQL**.
3. Create the database instance.
4. Copy the connection details into `DATABASE_URL` in your `.env` file, in
   the format shown in `.env.example`.

The application automatically appends `sslmode=require` to the connection
string if it is not already present, and runs the necessary checkpoint
table setup (`checkpointer.setup()`) on startup.

## Running the Application

```bash
python app.py
```

The server starts at `http://127.0.0.1:8000` with hot reload enabled.

Alternatively, run it directly with Uvicorn:

```bash
uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

Once running, open `http://127.0.0.1:8000` in a browser to use the web
interface.

## API Reference

### `GET /`

Returns the rendered frontend (`templates/index.html`).

### `POST /api/travel`

Runs the full agent pipeline for a given user request.

**Request body**

```json
{
  "message": "Plan a 5 days Dubai trip from Delhi with flights, hotels and sightseeing.",
  "thread_id": null
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `message` | `string` | Yes | The user's travel request. |
| `thread_id` | `string` \| `null` | No | An existing thread ID to continue a prior conversation. Omit or pass `null` to start a new thread. |

**Response body (success)**

```json
{
  "success": true,
  "thread_id": "user_3f9a1c2b...",
  "answer": "## Trip Summary\n...",
  "flight_results": "...",
  "hotel_results": "...",
  "itinerary": "...",
  "llm_calls": 3
}
```

| Field | Type | Description |
|---|---|---|
| `success` | `boolean` | Whether the request completed successfully. |
| `thread_id` | `string` | The thread ID for this conversation (generated if not provided). |
| `answer` | `string` | The Final Agent's consolidated, markdown-formatted travel plan. |
| `flight_results` | `string` | Raw output from the Flight Agent. |
| `hotel_results` | `string` | Raw output from the Hotel Agent. |
| `itinerary` | `string` | Raw output from the Itinerary Agent. |
| `llm_calls` | `integer` | Number of LLM invocations made while processing this request. |

**Response body (error)**

```json
{
  "success": false,
  "error": "Message cannot be empty."
}
```

| Status code | Condition |
|---|---|
| `200` | Request processed successfully. |
| `400` | `message` was empty or missing. |
| `500` | An unhandled exception occurred while running the agent pipeline. |

### `GET /health`

Health check endpoint.

```json
{
  "status": "ok",
  "message": "Tripo  API is running"
}
```

### `GET /favicon.ico`

Returns an empty JSON response to prevent unhandled 404s from browser
favicon requests.

## Frontend

The frontend (`templates/index.html`, `static/style.css`,
`static/script.js`) is a single-page interface served by FastAPI's Jinja2
templating and static file mounting. It communicates with the backend
exclusively through `POST /api/travel`.

Key behavior implemented in `static/script.js`:

- Submits the user's request and displays the returned plan, rendering
  markdown via `marked.js`.
- Maintains `thread_id` across requests using `localStorage`, allowing a
  session to persist across page reloads.
- Renders the Flight Agent, Hotel Agent, and Itinerary Agent outputs in
  separate tabs alongside the consolidated overview.
- Displays an animated agent-pipeline indicator while a request is in
  progress.
- Exports the full plan (all sections) to PDF using `html2pdf.js`.
- Stores recent prompts locally for quick re-use.

No changes to the frontend require any change to `app.py`, `backend.py`,
or `tools/`, since all data displayed by the UI is already present in the
`/api/travel` response schema.

## Testing

`test.py` provides a manual CLI harness for exercising the agent pipeline
directly, without the FastAPI layer:

```bash
python test.py
```

This will prompt for a travel request in the terminal, run it through
`run_travel_agent`, and print the final answer. It is intended for local
debugging of the LangGraph pipeline and tool integrations
(`tavily_search`, `search_flights`), not as an automated test suite.

## Troubleshooting

| Issue | Likely cause | Resolution |
|---|---|---|
| `ValueError: DATABASE_URL is missing` | `.env` file missing or not loaded | Confirm `.env` exists in the project root and contains `DATABASE_URL`. |
| `ValueError: GROQ_API_KEY is missing` | Missing or invalid Groq key | Set `GROQ_API_KEY` in `.env`. |
| PostgreSQL authentication error on startup | Incorrect password or unescaped special characters in `DATABASE_URL` | Verify credentials in the Render dashboard; URL-encode special characters in the password. |
| Flight or hotel results empty in the response | Upstream API (AviationStack/Tavily) rate-limited or returned no data | Check API key validity and usage limits on the respective provider dashboards. |
| Frontend shows "Something went wrong" | Backend returned a 500 | Check server logs/stack trace printed by `app.py`'s exception handler. |

## Roadmap

- Streaming responses so the frontend pipeline indicator reflects real
  agent progress instead of a fixed-interval simulation.
- Structured (JSON) outputs from the Flight and Hotel agents for richer
  frontend rendering (e.g., sortable flight/hotel cards).
- Automated test suite (`pytest`) covering `backend.py` and `tools/`.
- Support for multi-city itineraries.

## Contributing

Issues and pull requests are welcome. For significant changes, please open
an issue first to discuss the proposed change.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for
details.

## Author

**Abhay Chand**
GitHub: [@Abhay-Chand](https://github.com/Abhay-Chand)
