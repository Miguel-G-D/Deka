"""Health domain model."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class HealthStatus:
    """Service health snapshot."""

    status: str
    service: str

    def is_ok(self) -> bool:
        return self.status == "ok"
