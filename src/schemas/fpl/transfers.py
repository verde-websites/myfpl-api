from typing import List
from pydantic import BaseModel

class TransfersFPLResponse(BaseModel):
    element_in: int
    element_in_cost: int
    element_out: int
    element_out_cost: int
    entry: int
    event: int
    time: str



