from fastapi import APIRouter

from app.models.overview import OverviewSeasonSummary
from app.services.overview_service import OverviewService

router = APIRouter(
    prefix="/overview",
    tags=["Overview"]
)

service = OverviewService()

@router.get(
    "/season_summary",
    response_model=OverviewSeasonSummary
)
def get_overview_stat(
    league: str = "EPL",
    season: str = "2025",
):
    """
    Returns statistics used by the Overview page
    """

    return service.get_season_summary(
        league=league,
        season=season,
    )