
import datetime
from pydantic import BaseModel

# Get Fixtures Response
class Fixture(BaseModel):
    id: int
    minutes: int
    kickoff_time: datetime.datetime
    started: bool
    finished: bool
    finished_provisional: bool
    provisional_start_time: bool
    home_team_id: int
    away_team_id: int
    home_team_name: str
    away_team_name: str
    home_team_score: int
    away_team_score: int
    home_team_red_cards: int
    away_team_red_cards: int
    class Config:
        from_attributes = True

class GetFixturesResponse(BaseModel):
    fixtures: list[Fixture]
