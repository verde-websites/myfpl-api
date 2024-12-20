import pprint
from typing import List
from src.models import Player as PlayerDBModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_players(db: AsyncSession, players: List[int]):
    """
    Get the players from the database
    """

    players_query = await db.execute(select(PlayerDBModel).where(PlayerDBModel.fpl_tracker_id.in_(players)))
    players_list = players_query.scalars().all()
    return players_list