# src/models/manager_models.py

from pydantic import BaseModel
from typing import List, Optional

class Metadata(BaseModel):
    id: int
    manager_name: str
    team_name: str
    rank: int
    gameweek_rank: int
    points: int
    total_points: int

class Transfers(BaseModel):
    id: int
    element_in: int
    element_out: int
    event: int

class Players(BaseModel):
    player_id: int
    first_name: str
    last_name: str
    web_name: str
    position: str
    points: int
    value: float
    is_captain: bool
    is_vice_captain: bool
    multiplier: int

class GetManagerResponse(BaseModel):
    metadata: Metadata
    transfers: List[Transfers]
    players: List[Players]

#  {
#   metadata: {
#     team_name: "DILFC",
#     team_id: 6375110,
#     manager_name: "Matthew Flegg",
#     rank: 1000000,
#     gameweek_rank: 59000,
#     points: 53,
#     total_points: 875,
#   }
#   players: [
#     {
#       first_name: "Erling",
#       last_name: "Haaland",
#       web_name: "Haaland",
#       position: "Forward",
#       points: 6,
#       value: 15.0,
#       is_captain: true,
#       is_vice_captain: false,
#       multiplier: 1,
#     }
#   ]
#   transfers: [
#     {
#       transfers_made: 1,
#       players_ins: {
#         player_name: "Erling Haaland",
#         player_value: 1000000,
#       },
#       players_out: {
#         player_name: "Erling Haaland",
#         player_value: 1000000,
#       }
#     }
#   ]
# }
