from understatapi import UnderstatClient
from typing import Any
from collections.abc import KeysView
from typing import TypedDict
from pydantic import BaseModel
from devtools import pprint, debug

# leagues = ["EPL", "La_Liga", "Bundesliga", "Serie_A", "Ligue_1", "RFPL"]

### Overview Season Sunmary ###

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

def calculate_season_summary(league_data):
    """
    Calculate season summary stats from league_data
    Output:
    1. Total matches, total goals, total xG
    2. XG/Match, Goals/Match
    3. Home, Away and Draw matches and percentage
    4. Avg home xG and avg away xG
    """
    total_matches: int = len(league_data["dates"])
    total_goals: int = 0
    total_xg_pre_format: float = 0
    home_win: int = 0
    away_win: int = 0
    draws: int = 0
    total_home_xg: float = 0
    total_away_xg: float = 0

    for match in league_data["dates"]:
        goals = match["goals"]
        xg = match["xG"]

        # Goal
        h_goal = int(goals["h"])
        a_goal = int(goals["a"])
        total_goals += h_goal + a_goal

        # XG
        h_xg = float(xg["h"])
        a_xg = float(xg["a"])
        total_xg_pre_format += h_xg + a_xg
        total_home_xg += h_xg
        total_away_xg += a_xg

        # Used for calculate win percentage
        # Calculate total of home and away win
        if h_goal > a_goal:
            home_win += 1
        elif h_goal < a_goal:
            away_win += 1
        elif h_goal == a_goal:
            draws += 1

    return OverviewSeasonSummary(
        total_matches = total_matches,
        total_goals = total_goals,
        total_xg = float(round(total_xg_pre_format, 2)),
        xg_per_match = round(total_xg_pre_format / total_matches, 2),
        goal_per_match = round(total_goals / total_matches, 2),
        home_win = home_win,
        home_win_percentage = round(home_win / total_matches * 100, 1),
        away_win = away_win,
        away_win_percentage = round(away_win / total_matches * 100, 1),
        draws = draws,
        draw_percentage = round(draws / total_matches * 100, 1),
        avg_home_xg = round(total_home_xg / total_matches, 2),
        avg_away_xg = round(total_away_xg / total_matches, 2)
    )

def print_season_summary(league_data):
    s = calculate_season_summary(league_data)
    print("calculate_season_summary()")
    print(f"1. Total Matches: {s.total_matches} | Total Goals: {s.total_goals} | Total xG: {s.total_xg}")
    print(f"2. XG / Match: {s.xg_per_match} | Goals / Match: {s.goal_per_match}")
    print(f"3. Home Wins: {s.home_win} ({s.home_win_percentage}%) | Away Wins: {s.away_win} ({s.away_win_percentage}%) | Draws: {s.draws} ({s.draw_percentage}%)")
    print(f"4. Avg Home XG: {s.avg_home_xg} | Avg Away xG: {s.avg_away_xg}")
    #debug(s)
    #pprint(s)

### Overview Highest Scoring ###

class OverviewHighestScoring(BaseModel):
    match_id: int
    match_name: str
    h_goal: int
    a_goal: int

def calculate_highest_scoring(league_data):
    highest_scoring_match = {
        "match_id": 0,
        "match_name": "",
        "h_goal": 0,
        "a_goal": 0,
        "scoring": 0
    }

    for match in league_data["dates"]:
        home_team_name: str = str(match["h"]["title"])
        away_team_name: str = str(match["a"]["title"])
        match_name: str = f"{home_team_name} vs {away_team_name}"
        
        goals = match["goals"]
        h_goal = int(goals["h"])
        a_goal = int(goals["a"])

        current_scoring: int = h_goal + a_goal
        if current_scoring > highest_scoring_match["scoring"]:
            highest_scoring_match["match_id"] = int(match["id"])
            highest_scoring_match["match_name"] = match_name
            highest_scoring_match["h_goal"] = h_goal
            highest_scoring_match["a_goal"] = a_goal
            highest_scoring_match["scoring"] = current_scoring
            

    return OverviewHighestScoring(
        match_id=highest_scoring_match["match_id"],
        match_name=highest_scoring_match["match_name"],
        h_goal=highest_scoring_match["h_goal"],
        a_goal=highest_scoring_match["a_goal"]
    )

def print_highest_scoring(league_data):
    h = calculate_highest_scoring(league_data)
    print(f"calculate_highest_scoring()")
    print(f"Highest scoring match: {h.match_name}")
    print(f"Score: {h.h_goal} - {h.a_goal}")


### Main Function ###
understat = UnderstatClient()
league_data: dict[str, Any] = understat.league("Ligue_1")._get_data("2025")
#print_season_summary(league_data)
print_highest_scoring(league_data)


