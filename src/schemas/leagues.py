from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

class ClassicLeague(BaseModel):
    id: int
    league_name: str
    league_type: str
    league_scoring: str
    number_of_teams: Optional[int] = None
    rank: Optional[int] = None
    previous_rank: Optional[int] = None
    percentile_rank: Optional[int] = None

class H2HLeague(BaseModel):
    id: int

class GetManagerLeagueResponse(BaseModel):
    classic: List[ClassicLeague]
    h2h: List[H2HLeague] 

  
  