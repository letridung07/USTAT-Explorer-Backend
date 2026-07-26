from typing import Any

from understatapi import UnderstatClient

class UnderstatAPI:
    def __init__(self):

        self.client = UnderstatClient()

    def get_league_data(
        self,
        league: str,
        season: str,
    ) -> dict[str, Any]:
        
        return self.client.league(league)._get_data(season)