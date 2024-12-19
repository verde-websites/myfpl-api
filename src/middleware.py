from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .database import SessionLocal

async def get_db():
    """
    Yields an async database session with read/write perms
    """
    async with SessionLocal.begin() as db:
        yield db

DB = Annotated[AsyncSession, Depends(get_db)]