import pytest

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)

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
