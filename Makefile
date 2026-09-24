.PHONY: install up down migrate dev test test-down logs ps clean

# Install/sync Python dependencies
install:
	uv sync --locked

# Start development PostgreSQL
up:
	docker compose up -d --wait postgres

# Stop containers
down:
	docker compose --profile tests down

# Apply database migrations
migrate:
	uv run --locked alembic upgrade head

# Start full development environment
dev:
	docker compose up -d --wait postgres
	uv run --locked alembic upgrade head
	uv run --locked uvicorn app.main:app --reload

# Start test DB and run tests
test:
	docker compose --profile tests up -d --wait postgres_test
	uv run --locked alembic -x database=test upgrade head
	uv run --locked pytest

# Stop test database
test-down:
	docker compose --profile tests stop postgres_test

# PostgreSQL logs
logs:
	docker compose logs -f postgres

# Container status
ps:
	docker compose --profile tests ps

# Remove containers and volumes
clean:
	docker compose --profile tests down -v
