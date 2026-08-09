def get_goal_or_zero(goal: int | None) -> int:
    if goal is None:
        return 0
    else: return int(goal)

def get_xg_or_zero(xg: float | None) -> float:
    if xg is None:
        return 0
    else: return float(xg)