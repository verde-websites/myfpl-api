from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

class LeagueTypeEnum(str, Enum):
    GENERAL = 'general'
    PRIVATE = 'private'

class LeagueScoringEnum(str, Enum):
    CLASSIC = 'classic'
    HEAD_TO_HEAD = 'h2h'

class ClassicLeague(BaseModel):
    id: int
    league_name: str = Field(alias="name")
    league_type: LeagueTypeEnum
    league_scoring: LeagueScoringEnum = Field(alias="scoring")
    number_of_teams: Optional[int] = Field(default=None, alias="rank_count")
    rank: Optional[int] = Field(default=None, alias="entry_rank")
    previous_rank: Optional[int] = Field(default=None, alias="entry_last_rank")
    percentile_rank: Optional[int] = Field(default=None, alias="entry_percentile_rank")

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

    class Config:
        allow_population_by_field_name = True

class H2HLeague(BaseModel):
    id: int

class GetManagerLeagueResponse(BaseModel):
    classic: List[ClassicLeague]
    h2h: List[H2HLeague] 

  
  