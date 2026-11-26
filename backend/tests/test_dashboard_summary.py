"""Dashboard summary use-case tests with in-memory repository."""

from datetime import UTC, datetime

from backend.application.dashboard import GetDashboardSummary, ListProcesses
from backend.domain.client import Client
from backend.domain.process import Process, ProcessStatus, SpaceType
from backend.domain.ports import ClientRepository, ProcessRepository


class InMemoryClientRepository(ClientRepository):
    def __init__(self, clients: list[Client]) -> None:
        self._clients = {c.id: c for c in clients}

    def list_all(self) -> list[Client]:
        return list(self._clients.values())

    def get(self, client_id: str) -> Client | None:
        return self._clients.get(client_id)


class InMemoryProcessRepository(ProcessRepository):
    def __init__(self, processes: list[Process]) -> None:
        self._processes = list(processes)

    def list_all(self) -> list[Process]:
        return list(self._processes)


def _sample_data() -> tuple[InMemoryClientRepository, InMemoryProcessRepository]:
    clients = [
        Client(id="cli-1", name="Ana Pérez", phone="+5491100000001"),
        Client(id="cli-2", name="Bruno Díaz", phone="+5491100000002"),
    ]
    processes = [
        Process(
            id="proc-1",
            client_id="cli-1",
            status=ProcessStatus.INTERESTED,
            party_size=2,
            space_type=SpaceType.TABLE,
            received_at=datetime(2026, 11, 20, 10, 0, tzinfo=UTC),
            needs_human=True,
        ),
        Process(
            id="proc-2",
            client_id="cli-1",
            status=ProcessStatus.CONFIRMED,
            party_size=4,
            space_type=SpaceType.TERRACE,
            received_at=datetime(2026, 11, 21, 11, 0, tzinfo=UTC),
            needs_human=False,
        ),
        Process(
            id="proc-3",
            client_id="cli-2",
            status=ProcessStatus.RESERVED,
            party_size=6,
            space_type=SpaceType.BIRTHDAY,
            received_at=datetime(2026, 11, 21, 15, 0, tzinfo=UTC),
            needs_human=False,
        ),
    ]
    return InMemoryClientRepository(clients), InMemoryProcessRepository(processes)


def test_dashboard_summary_counts() -> None:
    clients, processes = _sample_data()
    summary = GetDashboardSummary(processes).execute()
    assert summary.total_processes == 3
    assert summary.interested_count == 1
    assert summary.reserved_count == 1
    assert summary.confirmed_count == 1
    assert summary.needs_human_count == 1
    assert summary.total_party_size == 12


def test_dashboard_activity_series_groups_by_day() -> None:
    _, processes = _sample_data()
    summary = GetDashboardSummary(processes).execute()
    by_day = {point.date: point.count for point in summary.activity_series}
    assert by_day["2026-11-20"] == 1
    assert by_day["2026-11-21"] == 2


def test_list_processes_includes_client_name() -> None:
    clients, processes = _sample_data()
    rows = ListProcesses(clients, processes).execute()
    assert len(rows) == 3
    ana = next(row for row in rows if row.process_id == "proc-1")
    assert ana.client_name == "Ana Pérez"
    assert ana.status == ProcessStatus.INTERESTED
    assert ana.needs_human is True
