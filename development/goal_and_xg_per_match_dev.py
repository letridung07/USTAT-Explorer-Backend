from understatapi import UnderstatClient
from typing import Any
from collections.abc import KeysView
from typing import TypedDict
from pydantic import BaseModel
from devtools import pprint, debug
import numpy as np

# Return
class OverviewGoalAndXGPerMatch(BaseModel):
    highest_goal_per_match: float
    lowest_goal_per_match: float
    average_goal_per_match: float
    highest_xg_per_match: float
    lowest_xg_per_match: float
    average_xg_per_match: float


def get_overview_goal_and_xg_per_match(
    season: str,
    league: str
    ) -> OverviewGoalAndXGPerMatch:
    """
    Find Goal per match and XG per match
    - Highest
    - Lowest
    - All-time average
    - League Avg (provided by overview already)

    Solution:
    - Loop through a league and all years (e.g. EPL, year 2014 -> 2025(current))
    - Find total Goal_per_match of each season and divide by number of seasons -> All-time average
    - In goal_per_match_list find highest
    - In goal_per_match_list find lowest
    """
    understat = UnderstatClient()

    # Create a year list based on selected year (from 2014)
    year_list = []
    for year in range(2014, int(season)):
        year_list.append(year)

    goal_per_match_list: list[float] = []
    xg_per_match_list: list[float] = []

    # Loop through previous years up to selected year for a selected league
    for year in year_list:
        league_data: dict[str, Any] = understat.league(league)._get_data(str(year))
        total_matches: int = len(league_data["dates"])
        total_goals: int = 0
        total_xg: float = 0.0

        # Find goal and xg of league within a season (year)
        for match in league_data["dates"]:
            # Goal
            goals = match["goals"]
            total_goals += int(goals["h"]) + int(goals["a"])

            # xG
            xg = match["xG"]
            total_xg += float(xg["h"]) + float(xg["a"])

        # Append to goal and xg per match lists
        goal_per_match: float = total_goals / total_matches    
        goal_per_match_list.append(goal_per_match)
        xg_per_match: float = total_xg / total_matches
        xg_per_match_list.append(xg_per_match)
        
    return OverviewGoalAndXGPerMatch(
        highest_goal_per_match = round(np.max(goal_per_match_list), 2),
        lowest_goal_per_match = round(np.min(goal_per_match_list), 2),
        average_goal_per_match = round(np.average(goal_per_match_list), 2),
        highest_xg_per_match = round(np.max(xg_per_match_list), 2),
        lowest_xg_per_match = round(np.min(xg_per_match_list), 2),
        average_xg_per_match = round(np.average(xg_per_match_list), 2)
    )

### Main Function ###
pprint(get_overview_goal_and_xg_per_match("2025","Bundesliga"))