from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models import Fixture as FixtureDBModel
from src.models import Team as TeamDBModel

async def get_fixtures_by_gameweek_id(db: AsyncSession, gameweek_id: int):
    fixtures_query = await db.execute(select(FixtureDBModel).where(FixtureDBModel.game_week_id == gameweek_id))
    fixtures_list = fixtures_query.scalars().all()
    return fixtures_list

async def get_teams_by_ids(db: AsyncSession, team_ids: list[int]):
    teams_query = await db.execute(select(TeamDBModel).where(TeamDBModel.id.in_(team_ids)))
    teams_list = teams_query.scalars().all()
    return teams_list
