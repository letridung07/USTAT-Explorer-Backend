from pydantic import BaseModel

class OverviewStat(BaseModel):
    total_matches: int
    total_goals: int