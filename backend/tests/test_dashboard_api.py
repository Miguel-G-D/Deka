"""API tests for dashboard endpoints."""

from pathlib import Path

from fastapi.testclient import TestClient

from backend.infrastructure.sqlite import bootstrap_database
from backend.presentation.deps import reset_connection
from backend.presentation.main import create_app


def test_dashboard_endpoints_return_seeded_data(
    tmp_path: Path,
    monkeypatch,
) -> None:
    db_path = tmp_path / "api.db"
    reset_connection()

    def _boot(_db_path: Path | None = None):
        return bootstrap_database(db_path)

    monkeypatch.setattr("backend.presentation.deps.bootstrap_database", _boot)

    with TestClient(create_app()) as client:
        summary = client.get("/api/dashboard/summary")
        assert summary.status_code == 200
        body = summary.json()
        assert body["total_processes"] == 10
        assert body["interested_count"] >= 1
        assert len(body["activity_series"]) >= 1

        processes = client.get("/api/processes")
        assert processes.status_code == 200
        rows = processes.json()
        assert len(rows) == 10
        assert any(row["client_name"] == "Ana Pérez" for row in rows)
        assert {
            "process_id",
            "status",
            "party_size",
            "space_type",
            "needs_human",
        } <= set(rows[0])

        clients = client.get("/api/clients")
        assert clients.status_code == 200
        assert len(clients.json()) == 5

    reset_connection()
