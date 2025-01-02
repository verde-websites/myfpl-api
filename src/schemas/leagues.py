import datetime
from typing import List, Optional
from pydantic import BaseModel

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
    admin_entry: Optional[int] = None
    start_event: Optional[int] = None
    code_privacy: Optional[str] = None
    has_cup: Optional[bool] = None
    cup_league: Optional[int] = None
    rank: Optional[int] = None
class GetLeagueResponse(BaseModel):
    metadata: LeagueMetadata
    standings: List[Entry]

  
  
