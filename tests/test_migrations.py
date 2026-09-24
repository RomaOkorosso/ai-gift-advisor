import os
from pathlib import Path
import subprocess
import sys

import pytest


PROJECT_ROOT = Path(__file__).resolve().parent.parent


@pytest.mark.parametrize("offline", [False, True])
@pytest.mark.parametrize(
    ("selector", "database", "expected_error"),
    [
        ("test", "gift_advisor", "Integration tests must use gift_advisor_test"),
        ("tests", "gift_advisor_test", "Unknown database environment: tests"),
    ],
)
def test_migrations_reject_unsafe_or_unknown_target(offline, selector, database, expected_error):
    # Synthetic settings: rejection must happen before any database connection.
    env = os.environ.copy()
    env.update(
        POSTGRES_USER="migration_guard_test",
        POSTGRES_PASSWORD="unused",
        POSTGRES_DB=database,
        POSTGRES_PORT="1",
    )
    command = [
        sys.executable, "-m", "alembic", "-x", f"database={selector}",
        "upgrade", "head",
    ]
    if offline:
        command.append("--sql")
    result = subprocess.run(
        command, cwd=PROJECT_ROOT, env=env, capture_output=True, text=True, timeout=15,
    )
    assert result.returncode != 0
    assert expected_error in result.stderr
