from http.client import HTTPException
from src import services

async def get_league(league_id: int):
    """
    Get the league
    - **league_id**: ID of the league
    """
    try:
        league = await services.get_league(league_id)
        return league
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
