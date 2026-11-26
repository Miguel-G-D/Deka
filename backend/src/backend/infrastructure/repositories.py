"""SQLite repository implementations."""

from __future__ import annotations

import sqlite3
from datetime import datetime

from backend.domain.client import Client
from backend.domain.process import Process, ProcessStatus, SpaceType


class SqliteClientRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def list_all(self) -> list[Client]:
        rows = self._connection.execute(
            "SELECT id, name, phone FROM clients ORDER BY name"
        ).fetchall()
        return [
            Client(id=row["id"], name=row["name"], phone=row["phone"])
            for row in rows
        ]

    def get(self, client_id: str) -> Client | None:
        row = self._connection.execute(
            "SELECT id, name, phone FROM clients WHERE id = ?",
            (client_id,),
        ).fetchone()
        if row is None:
            return None
        return Client(id=row["id"], name=row["name"], phone=row["phone"])


class SqliteProcessRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def list_all(self) -> list[Process]:
        rows = self._connection.execute(
            """
            SELECT
                id, client_id, status, party_size,
                space_type, received_at, needs_human
            FROM processes
            ORDER BY received_at DESC
            """
        ).fetchall()
        return [
            Process(
                id=row["id"],
                client_id=row["client_id"],
                status=ProcessStatus(row["status"]),
                party_size=int(row["party_size"]),
                space_type=SpaceType(row["space_type"]),
                received_at=datetime.fromisoformat(row["received_at"]),
                needs_human=bool(row["needs_human"]),
            )
            for row in rows
        ]
