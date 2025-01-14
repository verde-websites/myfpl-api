from http.client import HTTPException
from typing import Optional
from src import services

async def get_classic_league(league_id: int, page: Optional[int] = None):
    """
    Get the league
    - **league_id**: ID of the league
    - **page**: (Optional) Page number for pagination
    """
    try:
        league = await services.get_classic_league(league_id, page)
        if not league:
            raise HTTPException(status_code=404, detail="Something went wrong. No league found.")
        return league
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
