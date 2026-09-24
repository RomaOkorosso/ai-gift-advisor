# AI Gift Advisor

AI Gift Advisor is a backend service for generating personalized gift recommendations based on a user's description and budget.

The project is being built as a production-style backend application with FastAPI, PostgreSQL, SQLAlchemy, Alembic, Docker and, in the next stage, Google Gemini.

## Tech stack

- Python 3.14+
- FastAPI
- PostgreSQL 17
- SQLAlchemy 2.x (async)
- asyncpg
- Alembic
- Docker Compose
- Pydantic Settings
- pytest
- AnyIO
- HTTPX

## Current status

Implemented:

- FastAPI application structure
- request validation with Pydantic
- async PostgreSQL connection
- SQLAlchemy ORM model for gift requests
- Alembic migrations
- service layer
- FastAPI dependency injection
- separate PostgreSQL database for tests
- transaction rollback between database tests
- API tests with dependency overrides
- full integration test: HTTP -> FastAPI -> service -> PostgreSQL

Next milestone:

- Google Gemini integration
- structured AI responses validated with Pydantic
- gift recommendation generation
- error handling and provider abstraction

## Project structure

```text
ai-gift-advisor/
├── alembic/
│   ├── versions/
│   └── env.py
├── app/
│   ├── api/
│   │   ├── routers/
│   │   └── dependencies.py
│   ├── core/
│   │   └── config.py
│   ├── db/
│   │   ├── base.py
│   │   └── session.py
│   ├── models/
│   │   └── gift.py
│   ├── schemas/
│   │   └── gifts.py
│   ├── services/
│   │   └── gifts.py
│   └── main.py
├── tests/
│   ├── config.py
│   ├── conftest.py
│   ├── test_database.py
│   ├── test_gift_api.py
│   └── test_gift_integration.py
├── .env.example
├── .env.test.example
├── alembic.ini
├── compose.yml
└── pyproject.toml
```

## Local setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd ai-gift-advisor
```

### 2. Create a virtual environment

Make sure Python 3.14 or newer is installed.

```bash
python3.14 -m venv .venv
source .venv/bin/activate
```

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

### 3. Install dependencies

Install the project and development dependency group:

```bash
python -m pip install -e . --group dev
```

If your pip version does not support dependency groups yet, install the development tools separately:

```bash
python -m pip install -e .
python -m pip install pytest httpx anyio
```

### 4. Configure environment variables

Create the main environment file:

```bash
cp .env.example .env
```

Create the test environment file:

```bash
cp .env.test.example .env.test
```

Default local PostgreSQL configuration used by the project:

```dotenv
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=gift_advisor
POSTGRES_PORT=5432
```

Test database configuration:

```dotenv
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=gift_advisor_test
POSTGRES_PORT=5433
```

Do not commit `.env` or `.env.test`.

## Database

### Start the main PostgreSQL database

```bash
docker compose up -d
```

Check its status:

```bash
docker compose ps
```

### Apply database migrations

```bash
python -m alembic upgrade head
```

### Start the test PostgreSQL database

The test database is enabled through the `tests` Docker Compose profile:

```bash
docker compose --profile tests up -d
```

The databases use different local ports:

- main database: `127.0.0.1:5432`
- test database: `127.0.0.1:5433`

### Apply migrations to the test database

```bash
python -m alembic -x database=test upgrade head
```

## Run the API

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## Tests

Make sure the test PostgreSQL container is running and its migrations are applied.

Run the full test suite:

```bash
python -m pytest -v
```

The database integration tests use transactions and roll them back after each test so test data does not persist between tests.

## Useful Docker commands

Show running containers:

```bash
docker ps
```

Show project services:

```bash
docker compose ps
```

Stop project containers:

```bash
docker compose --profile tests down
```

Stop containers and delete project volumes:

```bash
docker compose --profile tests down -v
```

> Warning: `-v` deletes PostgreSQL data stored in Docker volumes.

## API

Current endpoint:

```text
POST /gift
```

Example request:

```json
{
  "budget": 3000,
  "description": "Friend likes programming, video games and science fiction"
}
```

The endpoint currently validates the request and stores it in PostgreSQL.

AI-generated recommendations will be added in the next development stage.

## Planned AI integration

Google Gemini will be used as the first LLM provider, with minimal API cost as a priority.

Planned architecture:

```text
HTTP request
    ↓
FastAPI router
    ↓
Gift service
    ↓
LLM client
    ↓
Google Gemini
    ↓
Structured response
    ↓
Pydantic validation
```

Future work will also include provider abstraction so another LLM can be added without rewriting the business logic.

## License

See `LICENSE`.
