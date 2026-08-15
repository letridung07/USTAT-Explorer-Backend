SPECIAL_MATCH_RESULTS = {
    # Nantes vs Toulouse (cancelled mid match due to weather)
    # But no more considered as isResult = False
    # "29840": {
    #     "h_goal": 0,
    #     "a_goal": 0,
    #     "h_xg": 0,
    #     "a_xg": 0,
    #     "outcome": "draw", # draw/home_win/away_win
    # }
}

def get_special_matches_stat(match_id: str):
    result = SPECIAL_MATCH_RESULTS.get(str(match_id))

    if result is None:
        return None

    return result