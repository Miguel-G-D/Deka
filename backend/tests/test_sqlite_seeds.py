"""SQLite schema and seed tests."""

from pathlib import Path

from backend.infrastructure.db import connect, init_schema
from backend.infrastructure.repositories import (
    SqliteClientRepository,
    SqliteProcessRepository,
)
from backend.infrastructure.seeds import seed_if_empty


def test_seed_is_idempotent(tmp_path: Path) -> None:
    db_path = tmp_path / "test.db"
    connection = connect(db_path)
    init_schema(connection)

    assert seed_if_empty(connection) is True
    assert seed_if_empty(connection) is False

    clients = SqliteClientRepository(connection).list_all()
    processes = SqliteProcessRepository(connection).list_all()
    assert len(clients) == 5
    assert len(processes) == 10
    assert any(c.name == "Ana Pérez" for c in clients)
    assert any(p.id == "proc-1" for p in processes)
