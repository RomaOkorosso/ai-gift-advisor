import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from tests.config import test_settings


async def main():
    engine = create_async_engine(
        test_settings.database_url,
        echo=False,
    )

    try:
        async with engine.connect() as connection:
            result = await connection.execute(
                text("SELECT current_database()")
            )

            print("Connected to:", result.scalar_one())
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
