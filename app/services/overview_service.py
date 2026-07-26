from app.clients.understat_client import UnderstatAPI
from app.models.overview import OverviewStat

class OverviewService:

    def __init__(self):

        self.understat = UnderstatAPI()

    def get_overview(
            self,
            league: str,
            season: str,
    ) -> OverviewStat:

        league_data = self.understat.get_league_data(
            league,
            season
        )

        #
        # Calculation code in here
        #
        
        return OverviewStat(
            total_matches=10,
            total_goals=10,
        )