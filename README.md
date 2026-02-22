# Use-Case Intelligence Platform (Modular Agentic Architecture)

This repository now contains a **backend** and **frontend** in separate folders, with a layered design and MCP server integration.

## Folder Structure

- `backend/`
  - `app/api`: REST contracts and routes.
  - `app/agents`: Agent orchestration logic (validation agent).
  - `app/services`: Application service layer.
  - `app/repositories`: Repository abstractions and provider implementations.
  - `app/providers`: Plug-and-play providers (FAISS, embedding provider).
  - `app/db`: SQLAlchemy models/session.
  - `app/mcp`: MCP server tools.
- `frontend/`
  - React + TypeScript UI for input collection, validation and dashboard visualization.

## Required User Inputs to Collect

### 1) Ingestion Inputs
- `title` (required): Unique use-case title.
- `description` (required): Business and technical problem statement.
- `lob` (required): Line of business owner.
- `contact_email` (optional): Partner contact when match found.
- `source_type` (required, default `manual`): ingestion source (`manual`, `api`, `webhook`, etc).
- `source_uri` (optional): link to repo/harness/webhook/API docs.

### 2) Validation Inputs
- `idea_title` (required)
- `idea_description` (required)
- `lob` (required)

### 3) Infrastructure Inputs
- Application/repo location
- Runtime namespace/tenant
- Existing data source connectivity (MongoDB/SQL/etc.)

These are available programmatically through `GET /api/required-inputs` and through MCP tool `required_user_inputs`.

## Architecture Principles Applied

- **SOLID + layered architecture**
  - Presentation (`api`) → Application service (`services`) → Domain (`domain`) → Infrastructure (`repositories`, `providers`).
- **Factory pattern** for provider/repository selection (`services/factories.py`).
- **Plug-and-play backends**
  - SQL defaults to SQLite but repository interface allows replacing with any SQL/NoSQL repository implementation.
  - Vector defaults to FAISS but `VectorStore` interface allows swapping providers.
- **Environment variable configuration** via `pydantic-settings`.

## Default Tech Choices

- Vector DB: **FAISS** (`VECTOR_PROVIDER=faiss`)
- SQL DB: **SQLite** (`SQL_DB_URL=sqlite:///./data/app.db`)
- MCP server: `backend/app/mcp/server.py`

## Run Instructions

### Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### MCP Server
```bash
cd backend
python -m app.mcp.server
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

- `GET /health`
- `GET /api/required-inputs`
- `POST /api/use-cases`
- `GET /api/use-cases`
- `POST /api/validate`
- `GET /api/dashboard`
