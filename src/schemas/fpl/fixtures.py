from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, validator
from datetime import datetime

class StatDetail(BaseModel):
    value: int
    element: int

class StatEntry(BaseModel):
    identifier: str
    a: List[StatDetail] = Field(default_factory=list)
    h: List[StatDetail] = Field(default_factory=list)

class FixtureFPLResponse(BaseModel):
    code: int
    event: int
    finished: bool
    finished_provisional: bool
    id: int
    kickoff_time: datetime
    minutes: int
    provisional_start_time: bool
    started: bool
    team_a: int
    team_a_score: Optional[int] = None
    team_h: int
    team_h_score: Optional[int] = None
    stats: List[StatEntry] = Field(default_factory=list)
    team_h_difficulty: int
    team_a_difficulty: int
    pulse_id: int

    @field_validator("team_a_score", "team_h_score", mode="before")
    def set_default_scores(cls, value):
        # If the JSON field is null, default to 0
        if value is None:
            return 0
        return value

class FixturesFPLResponse(BaseModel):
    fixtures: List[FixtureFPLResponse] = Field(alias="fixtures")
