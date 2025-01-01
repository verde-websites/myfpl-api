from pydantic import BaseModel, Field
from typing import List, Optional, Any

class Entry(BaseModel):
  id: int
  event_total: int
  player_name: str
  rank: int
  last_rank: int
  rank_sort: int
  total: int
  entry: int
  entry_name: str
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