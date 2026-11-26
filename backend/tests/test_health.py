"""Health use case and route tests."""

from fastapi.testclient import TestClient

from backend.application.health import GetHealthStatus
from backend.domain.health import HealthStatus
from backend.infrastructure.sqlite import default_db_path
from backend.presentation.main import create_app


def test_health_status_is_ok() -> None:
    status = GetHealthStatus().execute()
    assert isinstance(status, HealthStatus)
    assert status.is_ok()
    assert status.service == "deka-backend"


def test_health_endpoint() -> None:
    client = TestClient(create_app())
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "deka-backend"}


def test_default_db_path_ends_with_deka_db() -> None:
    path = default_db_path()
    assert path.name == "deka.db"
