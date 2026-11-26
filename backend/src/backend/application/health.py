"""Health use cases."""

from backend.domain.health import HealthStatus


class GetHealthStatus:
    """Return the API health status."""

    def execute(self) -> HealthStatus:
        return HealthStatus(status="ok", service="deka-backend")
