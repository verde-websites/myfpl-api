from typing import List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime

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
    name: str
    short_name: Optional[str] = None
    created: datetime
    closed: bool
    rank: Optional[int] = None
    max_entries: Optional[int] = None
    league_type: str
    scoring: str
    admin_entry: Optional[int] = None
    start_event: int
    entry_can_leave: bool
    entry_can_admin: bool
    entry_can_invite: bool
    has_cup: bool
    cup_league: Optional[int] = None
    cup_qualified: Optional[bool] = None
    rank_count: Optional[int] = None
    entry_percentile_rank: Optional[int] = None
    active_phases: List[ActivePhase]
    entry_rank: int
    entry_last_rank: int

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
    summary_event_rank: int
    current_event: int
    leagues: Leagues
    team_name: str = Field(alias="name")
    name_change_blocked: bool
    entered_events: List[int]
    kit: Optional[Any] = None  # Replace Any with a specific model if structure is known
    last_deadline_bank: int
    last_deadline_value: int
    last_deadline_total_transfers: int