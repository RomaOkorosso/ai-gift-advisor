import pytest

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.db.session import get_db

from tests.config import test_settings


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def engine(anyio_backend):
    engine = create_async_engine(
        test_settings.database_url,
        echo=False,
    )

    yield engine

    await engine.dispose()


@pytest.fixture
async def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    try:
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test",
        ) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(get_db, None)


@pytest.fixture
async def db_session(engine):
    async with engine.connect() as connection:
        transaction = await connection.begin()

        async with AsyncSession(
                bind=connection,
                join_transaction_mode="create_savepoint",
                expire_on_commit=False,
        ) as session:
            try:
                yield session
            finally:
                await transaction.rollback()
