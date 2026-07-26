from understatapi import UnderstatClient
import json
from typing import Any
from collections.abc import KeysView
from typing import TypedDict
from pydantic import BaseModel
# with open('league_data.json', 'w') as file:
#     json.dump(league_data, file)

class TeamDelta(BaseModel):
    team_id: int
    team_name: str
    total_scored: int
    total_xg: float
    delta: float

class HighestGoal(BaseModel):
    goals: int
    match_id: int
    match_name: str
    h_goal: int
    a_goal: int

class HighestXG(BaseModel):
    xg: float
    match_id: int
    match_name: str

class BiggestXGUpset(BaseModel):
    delta_xg: float
    match_id: int
    match_name: str
    win_team_name: str
    lose_team_name: str
    win_xg: float
    lose_xg: float



def calculate_season_summary(league_data):
    """
    Calculate season summary stats from league_data
    Output:
    1. Total matches, total goals, total xG
    2. XG/Match, Goals/Match
    3. Home, Away and Draw matches and percentage
    4. Avg home xG and avg awat xG
    """
    total_matches: int = len(league_data["dates"])
    
    total_goal: int = 0
    total_xg_pre_format: float = 0
    home_win: int = 0
    away_win: int = 0
    draws: int = 0
    total_home_xg: float = 0
    total_away_xg: float = 0

    highest_goal = HighestGoal(
        goals=0,
        match_id=0,
        match_name="",
        h_goal=0,
        a_goal=0,
    )
    highest_xg = HighestXG(
        xg=0.0,
        match_id=0,
        match_name="",
    )

    for i in range(0, total_matches):
        # Goals
        h_goal: int = int(league_data["dates"][i]["goals"]["h"])
        a_goal: int = int(league_data["dates"][i]["goals"]["a"])
        total_goal = total_goal + h_goal + a_goal
        # XG
        h_xg: float = float(league_data["dates"][i]["xG"]["h"])
        a_xg: float = float(league_data["dates"][i]["xG"]["a"])
        total_xg_pre_format = total_xg_pre_format + h_xg + a_xg
        total_home_xg += float(league_data["dates"][i]["xG"]["h"])
        total_away_xg += float(league_data["dates"][i]["xG"]["a"])

        # home and away: win and draw
        if h_goal > a_goal:
            home_win += 1
        if h_goal < a_goal:
            away_win += 1
        if h_goal == a_goal:
            draws += 1

        home_team_name: str = str(league_data["dates"][i]["h"]["title"])
        away_team_name: str = str(league_data["dates"][i]["a"]["title"])
        match_id: int = int(league_data["dates"][i]["id"])
        match_name: str = f"{home_team_name} vs {away_team_name}"
        # Highest goal match
        current_goal: int = h_goal + a_goal
        if current_goal > highest_goal.goals:
            highest_goal.goals = current_goal
            highest_goal.match_id = match_id
            highest_goal.match_name = match_name
            highest_goal.h_goal = h_goal
            highest_goal.a_goal = a_goal
        # Highest xg
        current_xg: float = float(round(h_xg + a_xg, 2))
        if current_xg > highest_xg.xg:
            highest_xg.xg = current_xg
            highest_xg.match_id = match_id
            highest_xg.match_name = match_name

    total_xg: float = float(round(total_xg_pre_format, 2))
    goal_over_match = round(total_goal / total_matches, 2)
    xg_over_match = round(total_xg_pre_format / total_matches, 2)
    home_win_percentage = round(home_win / total_matches * 100, 1)
    away_win_percentage = round(away_win / total_matches * 100, 1)
    draw_percentage = round(draws / total_matches * 100, 1)
    avg_home_xg = round(total_home_xg / total_matches, 2)
    avg_away_xg = round(total_away_xg / total_matches, 2)

    print("calculate_season_summary()")
    print(f"1. Total Matches: {total_matches} | Total Goals: {total_goal} | Total xG: {total_xg}")
    print(f"2. XG / Match: {xg_over_match} | Goals / Match: {goal_over_match}")
    print(f"3. Home Wins: {home_win} ({home_win_percentage}%) | Away Wins: {away_win} ({away_win_percentage}%) | Draws: {draws} ({draw_percentage}%)")
    print(f"4. Avg Home XG: {avg_home_xg} | Avg Away xG: {avg_away_xg}")
    



def overview_api():
    understat = UnderstatClient()
    league_data: dict[str, Any] = understat.league("EPL")._get_data("2025")
    total_matches: int = len(league_data["dates"])

    total_goal: int = 0
    total_xg_pre_format: float = 0
    home_win: int = 0
    away_win: int = 0
    draws: int = 0
    total_home_xg: float = 0
    total_away_xg: float = 0

    highest_goal = HighestGoal(
        goals=0,
        match_id=0,
        match_name="",
        h_goal=0,
        a_goal=0,
    )
    highest_xg = HighestXG(
        xg=0.0,
        match_id=0,
        match_name="",
    )
    biggest_xg_upset = BiggestXGUpset(
        delta_xg=0.0,
        match_id=0,
        match_name="",
        win_team_name="",
        lose_team_name="",
        win_xg=0.0,
        lose_xg=0.0,
    )

    for i in range(0, total_matches):
        # Goals
        h_goal: int = int(league_data["dates"][i]["goals"]["h"])
        a_goal: int = int(league_data["dates"][i]["goals"]["a"])
        total_goal = total_goal + h_goal + a_goal
        # XG
        h_xg: float = float(league_data["dates"][i]["xG"]["h"])
        a_xg: float = float(league_data["dates"][i]["xG"]["a"])
        total_xg_pre_format = total_xg_pre_format + h_xg + a_xg
        total_home_xg += float(league_data["dates"][i]["xG"]["h"])
        total_away_xg += float(league_data["dates"][i]["xG"]["a"])


        # home and away: win and draw
        if h_goal > a_goal:
            home_win += 1
        if h_goal < a_goal:
            away_win += 1
        if h_goal == a_goal:
            draws += 1

        home_team_name: str = str(league_data["dates"][i]["h"]["title"])
        away_team_name: str = str(league_data["dates"][i]["a"]["title"])
        match_id: int = int(league_data["dates"][i]["id"])
        match_name: str = f"{home_team_name} vs {away_team_name}"
        # Highest goal match
        current_goal: int = h_goal + a_goal
        if current_goal > highest_goal.goals:
            highest_goal.goals = current_goal
            highest_goal.match_id = match_id
            highest_goal.match_name = match_name
            highest_goal.h_goal = h_goal
            highest_goal.a_goal = a_goal
        # Highest xg
        current_xg: float = float(round(h_xg + a_xg, 2))
        if current_xg > highest_xg.xg:
            highest_xg.xg = current_xg
            highest_xg.match_id = match_id
            highest_xg.match_name = match_name
        
        # Match where the losing team had the highest expected goal (xg) advantage over winning team        
        current_delta_xg: float = h_xg - a_xg
        # Find upset matches
        if h_goal < a_goal and current_delta_xg > 0:
            # Find biggest delta xg in the list
            if current_delta_xg > biggest_xg_upset.delta_xg:
                biggest_xg_upset.delta_xg = round(current_delta_xg, 2)
                biggest_xg_upset.match_id = match_id
                biggest_xg_upset.match_name = match_name

                if h_goal > a_goal:
                    biggest_xg_upset.win_team_name = home_team_name
                    biggest_xg_upset.lose_team_name = away_team_name
                    biggest_xg_upset.win_xg = round(h_xg, 2)
                    biggest_xg_upset.lose_xg = round(a_xg, 2)
                elif h_goal < a_goal:
                    biggest_xg_upset.win_team_name = away_team_name
                    biggest_xg_upset.lose_team_name = home_team_name
                    biggest_xg_upset.win_xg = round(a_xg, 2)
                    biggest_xg_upset.lose_xg = round(h_xg, 2)

    total_xg: float = float(round(total_xg_pre_format, 2))
    goal_over_match = round(total_goal / total_matches, 2)
    xg_over_match = round(total_xg_pre_format / total_matches, 2)
    home_win_percentage = round(home_win / total_matches * 100, 1)
    away_win_percentage = round(away_win / total_matches * 100, 1)
    draw_percentage = round(draws / total_matches * 100, 1)
    avg_home_xg = round(total_home_xg / total_matches, 2)
    avg_away_xg = round(total_away_xg / total_matches, 2)

    # calculate_season_summary()
    print(f"Total Matches: {total_matches} | Total Goals: {total_goal}")
    print(f"Total xG: {total_xg} | Goals / Match: {goal_over_match}")
    print(f"Home Wins: {home_win} | Away Wins: {away_win} | Draws: {draws}")
    print(f"Home Win: {home_win_percentage}% | Away Win: {away_win_percentage}% | Draw: {draw_percentage}%")
    print(f"XG / Match: {xg_over_match} | Avg Home XG: {avg_home_xg} | Avg Away xG: {avg_away_xg}")

    # calculate_highlight_match()
    print(f"Highest goal match: {highest_goal.match_name} | Score: {highest_goal.h_goal}-{highest_goal.a_goal}")
    print(f"Highest XG match: {highest_xg.match_name} | Highest XG: {highest_xg.xg}")
    print(f"Biggest XG Upset: {biggest_xg_upset.match_name} | Delta XG: {biggest_xg_upset.delta_xg}")
    print(f"Despite {biggest_xg_upset.lose_team_name} having a higher xG ({biggest_xg_upset.lose_xg} to {biggest_xg_upset.win_xg}), {biggest_xg_upset.win_team_name} managed to win the match.")
    print(biggest_xg_upset)

    ### CLINICAL & WASTEFUL
    clinical = TeamDelta(
        total_scored=0,
        total_xg=0.0,
        team_id=0,
        team_name="",
        delta= 0.0,
    )
    wasteful = TeamDelta(
        total_scored=0,
        total_xg=0.0,
        team_id=0,
        team_name="",
        delta=99999.9,
    )
    list_of_team_ids: KeysView[str] = league_data["teams"].keys()
    for team_id in list_of_team_ids:
        total_team_history_matches: int = len(league_data["teams"][str(team_id)]["history"])
        total_scored: int = 0
        total_xg: float = 0
        for team_history_id in range(0, total_team_history_matches):
            scored: int = league_data["teams"][str(team_id)]["history"][int(team_history_id)]["scored"]
            xg: float = league_data["teams"][str(team_id)]["history"][int(team_history_id)]["xG"]
            total_scored += scored
            total_xg += xg

        scored_xg_delta: float = total_scored - total_xg
        if scored_xg_delta > clinical.delta:
            clinical.team_id = int(team_id)
            clinical.team_name = league_data["teams"][str(team_id)]["title"]
            clinical.total_scored = total_scored
            clinical.total_xg = total_xg
            clinical.delta = float(round(scored_xg_delta, 2))

        if scored_xg_delta < wasteful.delta:
            wasteful.team_id = int(team_id)
            wasteful.team_name = league_data["teams"][str(team_id)]["title"]
            wasteful.total_scored = total_scored
            wasteful.total_xg = total_xg
            wasteful.delta = float(round(scored_xg_delta, 2))

    # calculate_clinical_and_wasterful
    print(f"Most clinical: {clinical.team_name} | delta: {clinical.delta}")
    print(f"Most wasteful: {wasteful.team_name} | delta: {wasteful.delta}")

    # TODO: Refractor code into function blocks
    # TODO: Then: API for overview
    # TODO: Plotly graph => API: overview/plotly
    # TODO: API: Metadata

#overview_api()
understat = UnderstatClient()
league_data: dict[str, Any] = understat.league("EPL")._get_data("2025")

calculate_season_summary(league_data)