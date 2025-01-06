from typing import List, Optional, Any
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from enum import Enum

class LeagueScoringEnum(str, Enum):
    CLASSIC = 'classic'
    HEAD_TO_HEAD = 'h2h'

class LeagueTypeEnum(str, Enum):
    GENERAL = 'general'
    PRIVATE = 'private'

class ActivePhase(BaseModel):
    phase: int
    rank: int
    last_rank: int
    rank_sort: int
    total: int
    league_id: int
    rank_count: Optional[int] = None
    entry_percentile_rank: Optional[int] = None

class ClassicLeague(BaseModel):
    id: int
    league_name: str = Field(alias="name")
    short_name: Optional[str] = None
    created: datetime
    closed: bool
    rank: Optional[int] = None
    max_entries: Optional[int] = None
    league_type: LeagueTypeEnum
    league_scoring: LeagueScoringEnum = Field(alias="scoring")
    admin_entry: Optional[int] = None
    start_event: int
    entry_can_leave: bool
    entry_can_admin: bool
    entry_can_invite: bool
    has_cup: bool
    cup_league: Optional[int] = None
    cup_qualified: Optional[bool] = None
    number_of_teams: Optional[int] = Field(default=None, alias="rank_count")
    percentile_rank: Optional[int] = Field(default=None, alias="entry_percentile_rank")
    active_phases: List[ActivePhase]
    rank: int = Field(alias="entry_rank")
    previous_rank: int = Field(alias="entry_last_rank")
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


class CupMatch(BaseModel):
    id: int
    entry_1_entry: int
    entry_1_name: str
    entry_1_player_name: str
    entry_1_points: int
    entry_1_win: int
    entry_1_draw: int
    entry_1_loss: int
    entry_1_total: int
    entry_2_entry: int
    entry_2_name: str
    entry_2_player_name: str
    entry_2_points: int
    entry_2_win: int
    entry_2_draw: int
    entry_2_loss: int
    entry_2_total: int
    is_knockout: bool
    league: int
    winner: int
    seed_value: Optional[Any] = None
    event: int
    tiebreak: Optional[Any] = None
    is_bye: bool
    knockout_name: str



class CupStatus(BaseModel):
    qualification_event: Optional[int] = None
    qualification_numbers: Optional[int] = None
    qualification_rank: Optional[int] = None
    qualification_state: Optional[str] = None

class Cup(BaseModel):
    matches: List[Any]  # Replace Any with a specific model if structure is known
    status: CupStatus
    cup_league: Optional[int] = None

class CupMatch(BaseModel):
    id: int
    entry_1_entry: int
    entry_1_name: str
    entry_1_player_name: str
    entry_1_points: int
    entry_1_win: int
    entry_1_draw: int
    entry_1_loss: int
    entry_1_total: int
    entry_2_entry: int
    entry_2_name: str
    entry_2_player_name: str
    entry_2_points: int
    entry_2_win: int
    entry_2_draw: int
    entry_2_loss: int
    entry_2_total: int
    is_knockout: bool
    league: int
    winner: Optional[int] = None
    seed_value: Optional[Any] = None  # Specify type if known
    event: int
    tiebreak: Optional[Any] = None  # Specify type if known
    is_bye: bool
    knockout_name: str

class Leagues(BaseModel):
    classic: List[ClassicLeague]
    h2h: List[Any]
    cup: Cup
    cup_matches: List[CupMatch]

class EntryFPLResponse(BaseModel):
    id: int
    joined_time: datetime
    started_event: int
    favourite_team: int
    player_first_name: str
    player_last_name: str
    player_region_id: int
    player_region_name: str
    player_region_iso_code_short: str
    player_region_iso_code_long: str
    years_active: int
    summary_overall_points: int
    summary_overall_rank: int
    summary_event_points: int
    summary_event_rank: Optional[int] = None
    current_event: int
    leagues: Leagues
    team_name: str = Field(alias="name")
    name_change_blocked: bool
    entered_events: List[int]
    kit: Optional[Any] = None  # Replace Any with a specific model if structure is known
    last_deadline_bank: int
    last_deadline_value: int
    last_deadline_total_transfers: int