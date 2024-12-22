
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


class ChipPlay(BaseModel):
    chip_name: str
    num_played: int


class TopPlayerInfo(BaseModel):
    id: int
    points: int


class BootstrapStaticGameweeksResponse(BaseModel):
    id: int
    name: str
    deadline_time: datetime
    average_entry_score: int
    finished: bool
    data_checked: bool
    highest_scoring_entry: Optional[int] = 0
    deadline_time_epoch: int
    deadline_time_game_offset: int
    highest_score: Optional[int] = 0
    is_previous: bool
    is_current: bool
    is_next: bool
    cup_leagues_created: bool
    h2h_ko_matches_created: bool
    ranked_count: int
    chip_plays: List[ChipPlay]
    most_selected: Optional[int] = 0
    most_transferred_in: Optional[int] = 0
    top_player: Optional[int] = 0
    top_player_info: Optional[TopPlayerInfo] = 0
    transfers_made: int
    most_captained: Optional[int] = 0
    most_vice_captained: Optional[int] = 0
