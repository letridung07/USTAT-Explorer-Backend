# USTAT-Explorer-Backend

FastAPI backend bootstrap for USTAT Explorer.

## Prerequisites

- Python 3.11+

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
```

## Run locally

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --app-dir src --reload
```

## Test

```bash
pytest
```

## Lint and format checks

```bash
ruff check .
ruff format --check .
```

## Endpoints

- `GET /` - service metadata
- `GET /api/v1/health` - health check
- `GET /docs` - Swagger UI
