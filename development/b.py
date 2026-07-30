# Search for matches in league_data: isResult = false
from understatapi import UnderstatClient
from typing import Any
from devtools import pprint, debug
import json

leagues = ["EPL", "La_Liga", "Bundesliga", "Serie_A", "Ligue_1", "RFPL"]
seasons = [2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025]

understat = UnderstatClient()
# league_data: dict[str, Any] = understat.league("EPL")._get_data("2025")
# match_result = league_data["dates"][0]["isResult"]
# print(match_result)


match_false = []
for league in leagues:
    for season in seasons:
        league_data = understat.league(league)._get_data(season)
        print(f"Searching: league:{league}, season:{season}")
        
        for match in league_data["dates"]:
            #print(type(match["isResult"]))
            if match["isResult"] == False:
                print(match["isResult"])
                match_false.append(match)

print(len(match_false))

with open('match_result_false.json', 'w') as file:
    json.dump(match_false, file)



