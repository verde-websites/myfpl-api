from http.client import HTTPException
from typing import Optional
from src import services

async def get_league(league_id: int, page: Optional[int] = None):
    """
    Get the league
    - **league_id**: ID of the league
    - **page**: (Optional) Page number for pagination
    """
    try:
        league = await services.get_league(league_id, page)
        return league
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
