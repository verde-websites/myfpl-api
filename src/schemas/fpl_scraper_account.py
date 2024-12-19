
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class FPLScraperAccountSchema(BaseModel):
    """FPLScraperAccount model"""
    id: Optional[int]
    email: str
    password: str
    manager_id: str
    cookies: str
    in_use: bool
    last_used: Optional[datetime]
    cookies_last_updated: Optional[datetime]
    active: bool

    class Config:
        from_attributes = True