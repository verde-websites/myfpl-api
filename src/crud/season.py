from src.models import Season as SeasonDBModel
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.seasons import PostSeasons

async def get_season_by_id(session: AsyncSession, season_id: int) -> SeasonDBModel:
    """Get a season by id"""
    async with session:
        stmt = select(SeasonDBModel).where(SeasonDBModel.id == season_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

async def get_season_by_name(session: AsyncSession, season_name: str) -> SeasonDBModel:
    """Get a season by name"""
    stmt = select(SeasonDBModel).where(SeasonDBModel.season_name == season_name)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def get_seasons(session: AsyncSession) -> list[SeasonDBModel]:
    """Get all seasons"""
    stmt = select(SeasonDBModel)
    result = await session.execute(stmt)
    return result.scalars().all()

async def create_season(session: AsyncSession, season: PostSeasons):
    """Create a season"""
        # Step 1: Insert the season into the database
    stmt = insert(SeasonDBModel).values({SeasonDBModel.season_name: season.season_name})
    
    # Step 2: Execute the insert statement
    await session.execute(stmt)
    
    # Step 3: Commit the transaction to persist the data
    await session.commit()