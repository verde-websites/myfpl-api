from enum import Enum
from pydantic import BaseModel, Field, field_validator

class LeagueTypeEnum(str, Enum):
    GENERAL = 'general'
    PRIVATE = 'private'

class LeagueScoringEnum(str, Enum):
    CLASSIC = 'classic'
    HEAD_TO_HEAD = 'head_to_head'

class ClassicLeague(BaseModel):
    id: int
    league_name: str = Field(alias="name")
    league_type: LeagueTypeEnum
    league_scoring: LeagueScoringEnum
    number_of_teams: int = Field(alias="rank_count")
    rank: int = Field(alias="entry_rank")
    previous_rank: int = Field(alias="entry_last_rank")
    percentile_rank: int = Field(alias="entry_percentile_rank")

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

class HeadToHeadLeague(BaseModel):
    id: int

class GetManagerLeagueResponse(BaseModel):
    classic: ClassicLeague
    h2h: HeadToHeadLeague

  
  