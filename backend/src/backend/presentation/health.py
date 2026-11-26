"""Health HTTP routes."""

from fastapi import APIRouter

from backend.application.health import GetHealthStatus

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict[str, str]:
    status = GetHealthStatus().execute()
    return {"status": status.status, "service": status.service}
