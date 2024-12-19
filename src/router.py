
"""Creating the FastAPI router"""

from fastapi import APIRouter

from . import routes
from . import schemas

def seasons_router():
    """Build the seasons router"""
    router = APIRouter()
    router.get("/{season_id}", response_model=schemas.GetSeasonResponse)(routes.get_season)
    router.post("")(routes.post_season)
    return router

def gameweek_router():
    """Build the gameweek router"""
    router = APIRouter()
    router.get("/current", response_model=schemas.GetGameweekResponse)(routes.get_current_gameweek)
    return router

def build_router():
    """Build the FastAPI router"""
    router = APIRouter()
    router.include_router(seasons_router(), prefix="/api/seasons", tags=["seasons"])
    router.include_router(gameweek_router(), prefix="/api/gameweek", tags=["gameweek"])
    return router
