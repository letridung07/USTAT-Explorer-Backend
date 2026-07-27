from app.clients.understat_client import UnderstatAPI
from app.models.overview import OverviewSeasonSummary
from app.models.overview import OverviewHighestScoring
from devtools import pprint

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