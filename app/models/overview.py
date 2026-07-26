from pydantic import BaseModel

class OverviewStat(BaseModel):
    total_matches: int
    total_goals: int

class OverviewSeasonSummary(BaseModel):
    total_matches: int
    total_goals: int
    total_xg: float
    xg_per_match: float
    goal_per_match: float
    home_win: int
    home_win_percentage: float
    away_win: int
    away_win_percentage: float
    draws: int
    draw_percentage: float
    avg_home_xg: float
    avg_away_xg: float