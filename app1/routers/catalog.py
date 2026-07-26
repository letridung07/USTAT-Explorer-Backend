# For:
# League dropdown
# Season dropdown
# Team search or selector

from fastapi import APIRouter

router = APIRouter(
    tags=["Catalog"],
)


@router.get("/leagues")
def get_leagues():
    """Return all available leagues."""
    return 


@router.get("/seasons")
def get_seasons():
    """Return all available seasons."""
    return 


@router.get("/teams")
def get_teams(
    league: str = "EPL",
    season: int = 2025,
):
    """Return teams available for a league and season."""



    return