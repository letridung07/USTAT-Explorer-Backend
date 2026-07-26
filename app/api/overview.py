from fastapi import APIRouter

from app.models.overview import OverviewStat
from app.services.overview_service import OverviewService

router = APIRouter(
    prefix="/overview",
    tags=["Overview"]
)

service = OverviewService()

@router.get(
    "/stat",
    response_model=OverviewStat
)
def get_overview_stat(
    league: str = "EPL",
    season: str = "2025",
):
    """
    Returns statistics used by the Overview page
    """

    return service.get_overview(
        league=league,
        season=season,
    )