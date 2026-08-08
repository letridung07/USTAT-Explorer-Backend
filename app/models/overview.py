from pydantic import BaseModel

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

class OverviewHighestScoring(BaseModel):
    match_id: int
    match_name: str
    h_goal: int
    a_goal: int

class OverviewGoalAndXGPerMatch(BaseModel):
    selected_goal_per_match: float
    highest_goal_per_match: float
    lowest_goal_per_match: float
    average_goal_per_match: float
    selected_xg_per_match: float
    highest_xg_per_match: float
    lowest_xg_per_match: float
    average_xg_per_match: float