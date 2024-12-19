from src.models import Gameweek as GameweekDBModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_current_gameweek(db: AsyncSession):
    """
    Get the current gameweek
    """
    current_gameweek = await db.execute(select(GameweekDBModel).where(GameweekDBModel.gameweek_active == True))
    return current_gameweek.scalar_one_or_none()