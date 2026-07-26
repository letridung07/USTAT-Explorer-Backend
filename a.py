from understatapi import UnderstatClient

leagues = ['EPL', 'La_Liga', 'Bundesliga', 'Serie_A', 'Ligue_1', 'RFPL']

# Empty Dictionary {} with Type annotation
# - Key = league name (str)
# - Value = list of available seasons (list[str])
available_seasons: dict[str, list[str]] = {} 

with UnderstatClient() as understat:
    for league in leagues:
        # Empty list of string with Type annotation
        seasons: list[str] = []
        for year in range(2012, 2030):
            try:
                match = understat.league(league).get_team_data(str(year))
                if match != []:
                    seasons.append(str(year))
            except Exception:
                continue

        print(league,seasons)
        # Populate available_seasons: dict
        available_seasons[league] = seasons

# for key, value in available_seasons:
#     print(key)

key = available_seasons.keys()
value = available_seasons.values()

val = list(available_seasons.values())[0]

seasons = available_seasons["EPL"]

i = 0
i_season = []
for available_league, seasons in available_seasons.items():
    i = i + 1
    
