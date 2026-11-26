"""Domain layer: entities, value objects, ports."""

from backend.domain.client import Client
from backend.domain.health import HealthStatus
from backend.domain.process import Process, ProcessStatus, SpaceType

__all__ = [
    "Client",
    "HealthStatus",
    "Process",
    "ProcessStatus",
    "SpaceType",
]
