from fastapi import APIRouter

# Import OverviewService
from app.services.overview_service import OverviewService

# Import pydantic models
from app.models.overview import OverviewSeasonSummary
from app.models.overview import OverviewHighestScoring
from app.models.overview import OverviewGoalAndXGPerMatch

router = APIRouter(
    prefix="/overview",
    tags=["Overview"]
)

service = OverviewService()

@router.get(
    "/season_summary",
    response_model=OverviewSeasonSummary,
    operation_id="getSeasonSummary",
)
def get_overview_season_summary(
    league: str = "EPL",
    season: str = "2025",
):
    return service.get_season_summary(
        league=league,
        season=season,
    )

@router.get(
    "/highest_scoring",
    response_model=OverviewHighestScoring,
    operation_id="getHighestScoring",
)
def get_overview_highest_scoring(
    league: str = "EPL",
    season: str = "2025"
):
    return service.get_highest_scoring(
        league=league,
        season=season
    )

@router.get(
    "/scoring_overview",
    response_model=OverviewGoalAndXGPerMatch,
    operation_id="getScoringOverview",
)
def get_scoring_overview(
    league: str = "EPL",
    season: str = "2025"
):
    return service.get_overview_goal_and_xg_per_match(
        league=league,
        season=season
    )