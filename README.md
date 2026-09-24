# AI Gift Advisor

Backend for personalized gift recommendations. The API currently
validates, stores, and retrieves gift requests. The LLM integration
layer and structured recommendation contract are implemented, but a real
AI provider is not connected yet.

## Stack

Python 3.14+, FastAPI, PostgreSQL 17, async SQLAlchemy, Alembic, Docker
Compose, uv, pytest/AnyIO.

## Quick start

Install `uv`, Docker Engine with Docker Compose, and `make`.

From the project directory:

``` bash
cp .env.example .env
cp .env.test.example .env.test
make install
make dev
```

`make install` syncs the Python environment from `uv.lock`. `make dev`
starts PostgreSQL, applies migrations, and starts the API.

-   API: http://127.0.0.1:8000
-   Swagger UI: http://127.0.0.1:8000/docs

## Configuration

Development and test databases are configured separately using `.env`
and `.env.test`. Example configuration files are included in the
repository.

  Environment   Database              Local port
  ------------- --------------------- ------------
  Development   `gift_advisor`        5432
  Tests         `gift_advisor_test`   5433

Do not commit `.env` or `.env.test`.

SQL logging is disabled by default and can be enabled locally with
`SQL_ECHO=true`.

## Commands

  -----------------------------------------------------------------------
  Command                             Action
  ----------------------------------- -----------------------------------
  `make install`                      Sync dependencies from the lock
                                      file

  `make dev`                          Start the database, apply
                                      migrations, and run the API

  `make test`                         Start test PostgreSQL, apply test
                                      migrations, and run pytest

  `make up`                           Start development PostgreSQL

  `make migrate`                      Apply development database
                                      migrations

  `make test-down`                    Stop test PostgreSQL

  `make down`                         Stop both databases

  `make logs`                         Follow development database logs

  `make ps`                           Show container status

  `make clean`                        Remove containers and database
                                      volumes
  -----------------------------------------------------------------------

**`make clean` deletes data stored in the project database volumes.**

Tests use a separate PostgreSQL database and roll back test
transactions. LLM tests use fake providers and do not require an API key
or external calls.

## API

### Create a request

`POST /gift`

``` json
{
  "budget": 3000,
  "description": "Friend likes programming, video games and science fiction"
}
```

Returns `201` with `id`, `budget`, and `description`.

The budget must be a non-negative integer and defaults to `0` when
omitted. The description must contain 10--2000 characters after trimming
surrounding whitespace. Invalid input returns `422`.

### Retrieve a request

`GET /gift/{gift_id}`

Returns `200` with the saved request, `404` if it does not exist, or
`422` for an invalid ID.

Authentication and request ownership are not implemented yet.

## Architecture

The application keeps HTTP, database, and LLM-related logic separated:

``` text
HTTP API
   |
Gift Service --------> PostgreSQL
   |
Recommendation Service
   |
LLM Provider
```

The recommendation service depends on a provider interface rather than a
specific LLM SDK. This allows a real provider to be added without
coupling the application logic directly to it.

Additional implementation details and architectural decisions are
documented in [DEVELOPMENT.md](DEVELOPMENT.md).

## License

See [LICENSE](LICENSE).
