from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL

PROJECT_ROOT = Path(__file__).resolve().parent.parent


class TestSettings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_port: int

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env.test",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def database_url(self) -> str:
        if self.postgres_db != "gift_advisor_test":
            raise RuntimeError(
                "Integration tests must use gift_advisor_test database!"
            )
        url = URL.create(
            drivername="postgresql+asyncpg",
            username=self.postgres_user,
            password=self.postgres_password,
            host="127.0.0.1",
            port=self.postgres_port,
            database=self.postgres_db,
        )
        return url.render_as_string(hide_password=False)


test_settings = TestSettings()
