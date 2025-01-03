
from pydantic import BaseModel

class Fixture(BaseModel):
    id: int
    minutes: int
    home_team_id: int
    away_team_id: int
    home_team_name: str
    away_team_name: str
    home_team_score: int
    away_team_score: int
    home_team_red_cards: int
    away_team_red_cards: int

class GetFixturesResponse(BaseModel):
    fixtures: list[Fixture]
