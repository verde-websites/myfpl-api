import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

import datetime
from typing import List, Optional
from pydantic import BaseModel

from src.schemas.fpl.classic_league_standings import Entry
from src.schemas.fpl.entry import LeagueScoringEnum, LeagueTypeEnum

# GENERIC LEAGUE RESPONSE

class LeagueMetadata(BaseModel):
    id: int
    name: str
    created: str
    closed: bool
    max_entries: Optional[int] = None
    league_type: LeagueTypeEnum
    league_scoring: LeagueScoringEnum
    league_owner_id: int
    gameweek_created_at: int 
    # Not sure what these are used for, can readd if needed
    # code_privacy: Optional[str] = None
    # has_cup: Optional[bool] = None
    # cup_league: Optional[int] = None
    # rank: Optional[int] = None

class Team(BaseModel):
  id: int
  gameweek_total: int 
  manager_name: str 
  league_position: int 
  previous_league_position: int 
  rank_sort: int
  total_points: int 
  manager_id: int 
  team_name: str 
  has_played: bool
class GetLeagueResponse(BaseModel):
    metadata: LeagueMetadata
    standings: List[Team]

  
  
