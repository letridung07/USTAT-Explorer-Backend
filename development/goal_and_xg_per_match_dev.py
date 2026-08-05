from understatapi import UnderstatClient
from typing import Any
from collections.abc import KeysView
from typing import TypedDict
from pydantic import BaseModel
from devtools import pprint, debug

# Return
class OverviewGoalAndXGPerMatch(BaseModel):
    goal_per_match: float
    highest_goal_per_match: float
    lowest_goal_per_match: float
    alltime_avergage_goal_per_match: float
    xg_per_match: float
    highest_xg_per_match: float
    lowest_xg_per_match: float
    alltime_avergage_xg_per_match: float
    previous_search_highest_goal_per_match

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
    
    year_list = []
    for year in range(2014, int(season)):
        year_list.append(year)

    goal_per_match_list:list[dict] = []

    for year in year_list:
        total_matches: int = len(league_data["dates"])
        league_data: dict[str, Any] = understat.league(league)._get_data(str(year))
        for match in league_data["dates"]:
            # Goal
            h_goal = int(goals["h"])
            a_goal = int(goals["a"])
            total_goals += h_goal + a_goal
        goal_per_match = total_goals / total_matches    
        goal_per_match_list.append({})

    return year_list

### Main Function ###
print(get_overview_goal_and_xg_per_match("2025","EPL"))