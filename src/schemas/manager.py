# src/models/manager_models.py

from pydantic import BaseModel
from typing import List, Optional

class Metadata(BaseModel):
    id: int
    manager_name: str
    team_name: str
    gameweek_rank: int
    overall_rank: int
    points: int
    total_points: int
    team_value: int
    points_on_bench: int
    bank: int
    percentile_rank: int

class PlayerInDetails(BaseModel):
    player_in_id: int
    player_in_cost: int
    player_in_first_name: str
    player_in_second_name: str
    player_in_web_name: str

class PlayerOutDetails(BaseModel):
    player_out_id: int
    player_out_cost: int
    player_out_first_name: str
    player_out_second_name: str
    player_out_web_name: str

class TransferDetails(BaseModel):
    player_in: PlayerInDetails
    player_out: PlayerOutDetails

class Transfers(BaseModel):
    transfer_count: int
    details: List[TransferDetails]

class Players(BaseModel):
    fpl_tracker_id: int
    first_name: str
    second_name: str
    web_name: str
    position: str
    price: int
    status: str
    minutes: int
    total_points: int
    assists: int
    goals_scored: int
    own_goals: int
    yellow_cards: int
    red_cards: int
    bps_points: int
    team_id: int
    is_captain: bool
    is_vice_captain: bool
    multiplier: int
    team_position: int

class GetManagerResponse(BaseModel):
    metadata: Metadata
    transfers: Transfers
    players: List[Players]
