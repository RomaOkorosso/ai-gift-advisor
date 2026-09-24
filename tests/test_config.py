from sqlalchemy.engine import make_url

from app.core.config import Settings


def test_database_url_preserves_special_characters():
    settings = Settings(
        postgres_user="demo@user",
        postgres_password="p@ss:/%word",
        postgres_db="gift_advisor",
        _env_file=None,
    )
    url = make_url(settings.database_url)
    assert url.username == settings.postgres_user
    assert url.password == settings.postgres_password
    assert url.host == "127.0.0.1"
