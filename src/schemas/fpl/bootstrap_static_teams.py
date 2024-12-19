from pydantic import BaseModel


class BootstrapStaticTeamsResponse(BaseModel):
    code: int
    draw: int
    id: int
    loss: int
    name: str
    played: int
    points: int
    position: int
    short_name: str
    strength: int
    unavailable: bool
    win: int
    strength_overall_home: int
    strength_overall_away: int
    strength_attack_home: int
    strength_attack_away: int
    strength_defence_home: int
    strength_defence_away: int
    pulse_id: int
