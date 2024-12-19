from pydantic import BaseModel, Field
from typing import List

from .bootstrap_static_gameweeks import BootstrapStaticGameweeksResponse
from .bootstrap_static_players import BootstrapStaticPlayersResponse
from .bootstrap_static_teams import BootstrapStaticTeamsResponse


class GameSettings(BaseModel):
    league_join_private_max: int
    league_join_public_max: int
    league_max_size_public_classic: int
    league_max_size_public_h2h: int
    league_max_size_private_h2h: int
    league_max_ko_rounds_private_h2h: int
    league_prefix_public: str
    league_points_h2h_win: int
    league_points_h2h_lose: int
    league_points_h2h_draw: int
    league_ko_first_instead_of_random: bool
    squad_squadplay: int
    squad_squadsize: int
    squad_team_limit: int
    squad_total_spend: int
    ui_currency_multiplier: int
    ui_use_special_shirts: bool
    ui_special_shirt_exclusions: List[str]
    stats_form_days: int
    sys_vice_captain_enabled: bool
    transfers_cap: int
    transfers_sell_on_fee: float
    league_h2h_tiebreak_stats: List[str]
    timezone: str


class PlayerStatLabel(BaseModel):
    label: str
    name: str


class PlayerType(BaseModel):
    id: int
    plural_name: str
    plural_name_short: str
    singular_name: str
    singular_name_short: str
    squad_select: int
    squad_min_play: int
    squad_max_play: int
    ui_shirt_specific: bool
    sub_positions_locked: List[int]
    player_count: int = Field(alias="element_count")


class BootstrapStaticFPLResponse(BaseModel):
    gameweeks: List[BootstrapStaticGameweeksResponse] = Field(alias="events")
    game_settings: GameSettings
    teams: List[BootstrapStaticTeamsResponse]
    total_managers: int = Field(alias="total_players")
    players: List[BootstrapStaticPlayersResponse] = Field(alias="elements")
    player_stats: List[PlayerStatLabel] = Field(alias="element_stats")
    player_types: List[PlayerType] = Field(alias="element_types")
