from datetime import datetime

from pydantic import BaseModel


class GetGameweekResponse(BaseModel):
    id: int
    name: str
    transfer_deadline: datetime
    gameweek_active: bool
    gameweek_finished: bool
    data_checked: bool
