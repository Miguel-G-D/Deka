"""Dashboard HTTP routes."""

from fastapi import APIRouter

from backend.application.dashboard import (
    GetDashboardSummary,
    ListClients,
    ListProcesses,
)
from backend.presentation.deps import get_client_repo, get_process_repo

router = APIRouter(prefix="/api", tags=["dashboard"])


@router.get("/dashboard/summary")
def dashboard_summary() -> dict:
    summary = GetDashboardSummary(get_process_repo()).execute()
    return {
        "total_processes": summary.total_processes,
        "interested_count": summary.interested_count,
        "reserved_count": summary.reserved_count,
        "confirmed_count": summary.confirmed_count,
        "needs_human_count": summary.needs_human_count,
        "total_party_size": summary.total_party_size,
        "activity_series": [
            {"date": point.date, "count": point.count}
            for point in summary.activity_series
        ],
    }


@router.get("/processes")
def list_processes() -> list[dict]:
    rows = ListProcesses(get_client_repo(), get_process_repo()).execute()
    return [
        {
            "process_id": row.process_id,
            "client_id": row.client_id,
            "client_name": row.client_name,
            "status": row.status.value,
            "party_size": row.party_size,
            "space_type": row.space_type.value,
            "received_at": row.received_at,
            "needs_human": row.needs_human,
        }
        for row in rows
    ]


@router.get("/clients")
def list_clients() -> list[dict]:
    clients = ListClients(get_client_repo()).execute()
    return [
        {"id": client.id, "name": client.name, "phone": client.phone}
        for client in clients
    ]
