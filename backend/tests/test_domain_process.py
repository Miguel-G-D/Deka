"""Domain model tests for clients and processes."""

from datetime import UTC, datetime

from backend.domain.client import Client
from backend.domain.process import Process, ProcessStatus, SpaceType


def test_process_status_values() -> None:
    assert ProcessStatus.INTERESTED.value == "interested"
    assert ProcessStatus.RESERVED.value == "reserved"
    assert ProcessStatus.CONFIRMED.value == "confirmed"


def test_process_is_confirmed() -> None:
    process = Process(
        id="proc-1",
        client_id="cli-1",
        status=ProcessStatus.CONFIRMED,
        party_size=4,
        space_type=SpaceType.TERRACE,
        received_at=datetime(2026, 11, 1, 12, 0, tzinfo=UTC),
        needs_human=False,
    )
    assert process.is_confirmed()
    assert not process.needs_human


def test_client_identity() -> None:
    client = Client(id="cli-1", name="Ana Pérez", phone="+5491100000001")
    assert client.name == "Ana Pérez"
