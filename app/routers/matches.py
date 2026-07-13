# For:
# Match records

from fastapi import APIRouter

router = APIRouter(
    prefix="/matches",
    tags=["Matches"],
)


@router.get("")
def get_matches(
    league: str = "EPL",
    season: int = 2025,
    team: str | None = None,
):
    """Return matches for the selected league and season."""

    

    return