"""Creating the FastAPI router"""

from fastapi import APIRouter
from typing import Optional

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

def manager_router():
    """Build the manager router"""
    router = APIRouter()
    router.get("/{manager_id}", response_model=schemas.GetManagerResponse)(routes.get_manager)
    router.get("/{manager_id}/leagues", response_model=schemas.GetManagerLeagueResponse)(routes.get_manager_leagues)
    return router

def league_router():
    """Build the league router"""
    router = APIRouter()
    # TODO:response_model=schemas.GetLeagueResponse
    # Leagues Classic Endpoint FPL Side
    # router.get("/{league_id}")(routes.get_league)
    return router

def build_router():
    """Build the FastAPI router"""
    router = APIRouter()
    router.include_router(seasons_router(), prefix="/api/seasons", tags=["seasons"])
    router.include_router(gameweek_router(), prefix="/api/gameweek", tags=["gameweek"])
    router.include_router(manager_router(), prefix="/api/manager", tags=["manager"])
    router.include_router(league_router(), prefix="/api/league", tags=["league"])
    return router
