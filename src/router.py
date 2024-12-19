
"""Creating the FastAPI router"""

from fastapi import APIRouter

from . import routes
from .schemas import GetSeasonResponse, PostSeasons
from .routes import get_season, post_season

def seasons_router():
    """Build the seasons router"""
    router = APIRouter()
    router.get("/{season_id}", response_model=GetSeasonResponse)(routes.get_season)
    router.post("")(routes.post_season)
    return router

def build_router():
    """Build the FastAPI router"""
    router = APIRouter()
    router.include_router(seasons_router(), prefix="/api/seasons", tags=["seasons"])
    return router
