"""Idempotent SQLite seeds for the pilot dashboard."""

from __future__ import annotations

import sqlite3

SEED_CLIENTS = [
    ("cli-1", "Ana Pérez", "+5491100000001"),
    ("cli-2", "Bruno Díaz", "+5491100000002"),
    ("cli-3", "Carla Gómez", "+5491100000003"),
    ("cli-4", "Diego Ruiz", "+5491100000004"),
    ("cli-5", "Elena Soto", "+5491100000005"),
]

SEED_PROCESSES = [
    ("proc-1", "cli-1", "interested", 2, "table", "2026-11-18T10:00:00+00:00", 1),
    ("proc-2", "cli-1", "confirmed", 4, "terrace", "2026-11-19T12:30:00+00:00", 0),
    ("proc-3", "cli-2", "reserved", 6, "birthday", "2026-11-19T15:00:00+00:00", 0),
    ("proc-4", "cli-2", "interested", 3, "table", "2026-11-20T09:15:00+00:00", 1),
    ("proc-5", "cli-3", "confirmed", 2, "terrace", "2026-11-20T11:00:00+00:00", 0),
    ("proc-6", "cli-3", "reserved", 5, "table", "2026-11-21T13:45:00+00:00", 0),
    ("proc-7", "cli-4", "interested", 8, "birthday", "2026-11-21T16:00:00+00:00", 1),
    ("proc-8", "cli-4", "confirmed", 2, "table", "2026-11-22T10:20:00+00:00", 0),
    ("proc-9", "cli-5", "reserved", 4, "terrace", "2026-11-22T18:00:00+00:00", 0),
    ("proc-10", "cli-5", "confirmed", 3, "table", "2026-11-23T09:00:00+00:00", 0),
]


def seed_if_empty(connection: sqlite3.Connection) -> bool:
    """Insert pilot seeds when tables are empty. Returns True if seeded."""
    client_count = connection.execute("SELECT COUNT(*) FROM clients").fetchone()[0]
    if client_count > 0:
        return False

    connection.executemany(
        "INSERT INTO clients (id, name, phone) VALUES (?, ?, ?)",
        SEED_CLIENTS,
    )
    connection.executemany(
        """
        INSERT INTO processes (
            id, client_id, status, party_size, space_type, received_at, needs_human
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        SEED_PROCESSES,
    )
    connection.commit()
    return True
