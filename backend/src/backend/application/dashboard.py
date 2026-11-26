"""Dashboard use cases."""

from collections import Counter

from backend.domain.dashboard import ActivityPoint, DashboardSummary, ProcessRow
from backend.domain.ports import ClientRepository, ProcessRepository
from backend.domain.process import ProcessStatus


class GetDashboardSummary:
    def __init__(self, processes: ProcessRepository) -> None:
        self._processes = processes

    def execute(self) -> DashboardSummary:
        items = self._processes.list_all()
        status_counts = Counter(p.status for p in items)
        by_day: Counter[str] = Counter()
        for process in items:
            by_day[process.received_at.date().isoformat()] += 1
        series = tuple(
            ActivityPoint(date=day, count=count)
            for day, count in sorted(by_day.items())
        )
        return DashboardSummary(
            total_processes=len(items),
            interested_count=status_counts[ProcessStatus.INTERESTED],
            reserved_count=status_counts[ProcessStatus.RESERVED],
            confirmed_count=status_counts[ProcessStatus.CONFIRMED],
            needs_human_count=sum(1 for p in items if p.needs_human),
            total_party_size=sum(p.party_size for p in items),
            activity_series=series,
        )


class ListProcesses:
    def __init__(
        self,
        clients: ClientRepository,
        processes: ProcessRepository,
    ) -> None:
        self._clients = clients
        self._processes = processes

    def execute(self) -> list[ProcessRow]:
        clients = {c.id: c for c in self._clients.list_all()}
        rows: list[ProcessRow] = []
        for process in self._processes.list_all():
            client = clients.get(process.client_id)
            rows.append(
                ProcessRow(
                    process_id=process.id,
                    client_id=process.client_id,
                    client_name=client.name if client else "Unknown",
                    status=process.status,
                    party_size=process.party_size,
                    space_type=process.space_type,
                    received_at=process.received_at.isoformat(),
                    needs_human=process.needs_human,
                )
            )
        rows.sort(key=lambda row: row.received_at, reverse=True)
        return rows


class ListClients:
    def __init__(self, clients: ClientRepository) -> None:
        self._clients = clients

    def execute(self):
        return self._clients.list_all()
