from typing import List, Optional
from pydantic import BaseModel, Field

class AutomaticSub(BaseModel):
    manager_id: int = Field(alias="entry")
    player_in_id: int = Field(alias="element_in")
    player_out_id: int = Field(alias="element_out")
    gameweek_id: int = Field(alias="event")

class Picks(BaseModel):
    player_tracker_id: int = Field(alias="element")
    position: int
    multiplier: int
    is_captain: bool
    is_vice_captain: bool
    position: int = Field(alias="element_type")

class Entry(BaseModel):
    event: int
    points: int
    total_points: int
    rank: int
    rank_sort: int
    overall_rank: int
    percentile_rank: int
    bank: int
    value: int
    event_transfers: int
    event_transfers_cost: int
    points_on_bench: int

class PicksFPLResponse(BaseModel):
    active_chip: Optional[str] = None
    automatic_subs: List[AutomaticSub]
    entry_history: Entry
    picks: List[Picks]