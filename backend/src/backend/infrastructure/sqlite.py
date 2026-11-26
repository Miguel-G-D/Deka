"""SQLite path helpers and database bootstrap."""

from pathlib import Path

from backend.infrastructure.db import connect, init_schema
from backend.infrastructure.seeds import seed_if_empty


def default_db_path() -> Path:
    """Return the default SQLite file path for local development."""
    return Path("backend") / "data" / "deka.db"


def bootstrap_database(db_path: Path | None = None):
    path = db_path or default_db_path()
    connection = connect(path)
    init_schema(connection)
    seed_if_empty(connection)
    return connection
