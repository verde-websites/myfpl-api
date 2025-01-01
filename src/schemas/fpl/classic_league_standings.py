from pydantic import BaseModel, Field
from typing import List, Optional, Any

class Entry(BaseModel):
  id: int
  gameweek_total: int = Field(alias="event_total")
  manager_name: str = Field(alias="player_name")
  league_position: int = Field(alias="rank")
  previous_league_position: int = Field(alias="last_rank")
  rank_sort: int
  total_points: int = Field(alias="total")
  manager_id: int = Field(alias="entry")
  team_name: str = Field(alias="entry_name")
  has_played: bool

class NewEntries(BaseModel):
  has_next: bool
  page: int
  results: List[Entry]

class League(BaseModel):
  id: int
  name: str
  created: str
  closed: bool
  max_entries: Optional[int] = None
  league_type: str
  scoring: str
  admin_entry: int
  start_event: int
  code_privacy: str
  has_cup: bool
  cup_league: Optional[int] = None
  rank: Optional[int] = None

class Standings(BaseModel):
    has_next: bool
    page: int
    results: List[Entry]

class ClassicLeagueStandings(BaseModel):
  new_entries: NewEntries
  last_updated_date: str
  league: League
  standings: Standings