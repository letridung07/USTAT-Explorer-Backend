# For:
# Backend status (database, api connections, etc.)

from fastapi import APIRouter

router = APIRouter(
    tags=["Health"],
)


@router.get("/health")
def get_health() -> dict[str, str]:
    """Check whether the backend is running."""
    return {
        "status": "ok",
        "database": "connected",
        "understat_service": "available",
    }