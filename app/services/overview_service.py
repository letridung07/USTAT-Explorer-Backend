# Import BaseModels
from app.models.overview import OverviewSeasonSummary
from app.models.overview import OverviewHighestScoring
from app.models.overview import OverviewGoalAndXGPerMatch
from app.clients.understat_client import UnderstatAPI
from app.utils.overview_utils import get_goal_or_zero, get_xg_or_zero

# Import libraries
import numpy as np
import datetime
from devtools import pprint

import logging
logger = logging.getLogger(__name__)

class OverviewService:

    def __init__(self):

        self.understat = UnderstatAPI()

    def get_season_summary(
            self, 
            league: str, 
            season: str
        ) -> OverviewSeasonSummary:
        """
        Calculate season summary stats from league_data
        Output:
            1. Total matches, total goals, total xG
            2. XG/Match, Goals/Match
            3. Home, Away and Draw matches and percentage
            4. Avg home xG and avg away xG
        """
        league_data = self.understat.get_league_data(league, season)

        total_matches: int = len(league_data["dates"])
        total_goals: int = 0
        total_xg_pre_format: float = 0
        home_win: int = 0
        away_win: int = 0
        draws: int = 0
        total_home_xg: float = 0
        total_away_xg: float = 0
        datetime_now = datetime.datetime.now()
        completed_matches: int = 0
        upcoming_matches: int = 0
        cancelled_matches: int = 0

        for match in league_data["dates"]:
            # Convert match datetime to object
            match_datetime = datetime.datetime.strptime(
                match["datetime"],
                "%Y-%m-%d %H:%M:%S"
            )

            # Matches: completed, upcoming and cancelled
            if match["isResult"] == True and match_datetime < datetime_now:
                completed_matches += 1
            elif match["isResult"] == False and match_datetime >= datetime_now:
                upcoming_matches += 1
            elif match["isResult"] == False and match_datetime < datetime_now:
                cancelled_matches += 1           
  
            goals = match["goals"]
            xg = match["xG"]
    
            # Goal
            h_goal = get_goal_or_zero((goals["h"]))
            a_goal = get_goal_or_zero((goals["a"]))
            total_goals += h_goal + a_goal
    
            # XG
            h_xg = get_xg_or_zero((xg["h"]))
            a_xg = get_xg_or_zero((xg["a"]))
            total_xg_pre_format += h_xg + a_xg
            total_home_xg += h_xg
            total_away_xg += a_xg
    
            # Used for calculate win percentage
            # Calculate total of home and away win
            # Handle case: cancelled match (due to Covid)
            if match["isResult"] == True:
                if h_goal > a_goal:
                    home_win += 1
                elif h_goal < a_goal:
                    away_win += 1
                elif h_goal == a_goal:
                    draws += 1

            # TODO: Figure out what to do with cancelled match due to external events(weather,...) (isResult==False)
            # Count toward statistic or not        
            # elif match["isResult"] == False and goals["h"] != None and goals["a"] != None:
            #     # TODO
    
        return OverviewSeasonSummary(
            completed_matches = completed_matches,
            upcoming_matches = upcoming_matches,
            cancelled_matches = cancelled_matches,
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

    def get_highest_scoring(self, 
            league: str, 
            season: str
        ) -> OverviewHighestScoring:
        """
        Calculate highest scoring match of a season
        Output:
            1. match_name: Name of highest scoring match
            2. match_id: ID of highest scoring match
            3. h_goal: Match home score 
            4. a_goal: Match away score 
        """
        league_data = self.understat.get_league_data(league, season)

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

    def get_overview_goal_and_xg_per_match(
        self,
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
        # Create a year list based on selected year (from 2014)
        year_list: list[int] = []
        for year in range(2014, int(season)+1):
            year_list.append(year)

        goal_per_match_list: list[float] = []
        xg_per_match_list: list[float] = []

        # Loop through previous years up to selected year for a selected league
        for year in year_list:
            league_data = self.understat.get_league_data(league, str(year))
            total_matches: int = len(league_data["dates"])
            total_goals: int = 0
            total_xg: float = 0.0

            # Find goal and xg of league within a season (year)
            for match in league_data["dates"]:
                # Goal
                goals = match["goals"]
                total_goals += get_goal_or_zero(goals["h"]) + get_goal_or_zero(goals["a"])
                # xG
                xg = match["xG"]
                total_xg += get_xg_or_zero(xg["h"]) + get_xg_or_zero(xg["a"])

            # Append to goal and xg per match lists
            goal_per_match: float = total_goals / total_matches    
            goal_per_match_list.append(goal_per_match)
            xg_per_match: float = total_xg / total_matches
            xg_per_match_list.append(xg_per_match)

        # Selected goal and xg per match is the last item of their corresponding list -> list[-1]

        return OverviewGoalAndXGPerMatch(
            selected_goal_per_match = round(goal_per_match_list[-1], 2),
            highest_goal_per_match = round(np.max(goal_per_match_list), 2),
            lowest_goal_per_match = round(np.min(goal_per_match_list), 2),
            average_goal_per_match = round(np.average(goal_per_match_list), 2),
            selected_xg_per_match = round(xg_per_match_list[-1], 2),
            highest_xg_per_match = round(np.max(xg_per_match_list), 2),
            lowest_xg_per_match = round(np.min(xg_per_match_list), 2),
            average_xg_per_match = round(np.average(xg_per_match_list), 2)
        )

    # def get_overview(
    #         self,
    #         league: str,
    #         season: str,
    # ) -> OverviewStat:

    #     league_data = self.understat.get_league_data(
    #         league,
    #         season
    #     )

    #     #
    #     # Calculation code in here
    #     #
        
    #     return OverviewStat(
    #         total_matches=10,
    #         total_goals=10,
    #     )