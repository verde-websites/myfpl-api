from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models import Fixture as FixtureDBModel

async def get_fixtures_by_gameweek_id(db: AsyncSession, gameweek_id: int):
    fixtures_query = await db.execute(select(FixtureDBModel).where(FixtureDBModel.game_week_id == gameweek_id))
    fixtures_list = fixtures_query.scalars().all()
    return fixtures_list