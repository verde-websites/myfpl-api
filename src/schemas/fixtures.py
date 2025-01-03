
from pydantic import BaseModel

class Fixture(BaseModel):
    id: int
    home_team: str
    away_team: str
    home_score: int
    away_score: int

class GetFixturesResponse(BaseModel):
    fixtures: list[Fixture]
