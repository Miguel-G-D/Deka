"""Shared presentation dependencies."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass, field
from pathlib import Path

from backend.application.inbound import HandleInboundMessage
from backend.infrastructure.meta_client import MetaGraphClient
from backend.infrastructure.meta_settings import MetaSettings, load_meta_settings
from backend.infrastructure.repositories import (
    SqliteClientRepository,
    SqliteProcessRepository,
)
from backend.infrastructure.sqlite import bootstrap_database
from backend.infrastructure.stub_handler import StubEchoHandler


@dataclass
class _DbState:
    connection: sqlite3.Connection | None = field(default=None)


_STATE = _DbState()


def get_connection(db_path: Path | None = None) -> sqlite3.Connection:
    if _STATE.connection is None:
        _STATE.connection = bootstrap_database(db_path)
    return _STATE.connection


def reset_connection() -> None:
    if _STATE.connection is not None:
        _STATE.connection.close()
    _STATE.connection = None


def get_client_repo() -> SqliteClientRepository:
    return SqliteClientRepository(get_connection())


def get_process_repo() -> SqliteProcessRepository:
    return SqliteProcessRepository(get_connection())


def get_meta_settings() -> MetaSettings:
    return load_meta_settings()


def get_inbound_use_case() -> HandleInboundMessage:
    meta = get_meta_settings()
    return HandleInboundMessage(
        StubEchoHandler(),
        MetaGraphClient(
            page_access_token=meta.page_access_token,
            api_version=meta.api_version,
        ),
    )
