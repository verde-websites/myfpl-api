#from src.dependencies.core import DBSessionDep
from .. middleware import DB
from fastapi import HTTPException

from .. import crud
from ..schemas.seasons import PostSeasons

async def get_season(season_id: int, db: DB):
    """
    Get a season by id
    """
    s = await crud.get_season_by_id(db, season_id)
    if not s:
        raise HTTPException(status_code=404, detail="Season not found")
    return s

async def post_season(postSeasons: PostSeasons, db: DB):
    """
    Create a season
    """
    print("SEAON NAME: ", postSeasons.season_name)
    existing_season = await crud.get_season_by_name(db, postSeasons.season_name)
    if existing_season:
        raise HTTPException(status_code=400, detail="Season already exists")
    return await crud.create_season(db, postSeasons)