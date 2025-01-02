from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Any

from src.schemas.fpl.entry import LeagueScoringEnum, LeagueTypeEnum

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
  has_next: Optional[bool] = False
  page: int
  results: Optional[List[Entry]] = None

class League(BaseModel):
  id: int
  name: str
  created: str
  closed: bool
  max_entries: Optional[int] = None
  league_type: LeagueTypeEnum
  league_scoring: LeagueScoringEnum = Field(alias="scoring")
  league_owner_id: Optional[int] = Field(alias="admin_entry")
  gameweek_created_at: int = Field(alias="start_event")
  code_privacy: str
  has_cup: bool
  cup_league: Optional[int] = None
  rank: Optional[int] = None
  @field_validator('league_scoring', mode='before')
  def map_league_scoring(cls, value):
      mapping = {
          'c': LeagueScoringEnum.CLASSIC,
          'h': LeagueScoringEnum.HEAD_TO_HEAD
      }
      return mapping.get(value.lower(), value)

  @field_validator('league_type', mode='before')
  def map_league_type(cls, value):
      mapping = {
          's': LeagueTypeEnum.GENERAL,
          'x': LeagueTypeEnum.PRIVATE
      }
      return mapping.get(value.lower(), value)

class Standings(BaseModel):
    has_next: Optional[bool] = False
    page: int
    results: Optional[List[Entry]] = None

class ClassicLeagueStandingsResponse(BaseModel):
  new_entries: NewEntries
  last_updated_data: str
  league: League
  standings: Standings