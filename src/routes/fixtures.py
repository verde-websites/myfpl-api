from http.client import HTTPException
from src import services
from src.middleware import DB

async def get_fixtures(db: DB, gameweek_id: int):
    """
    Get the fixtures
    - **gameweek_id**: ID of the gameweek
    """
    try:
        fixtures = await services.get_fixtures(db, gameweek_id)
        return fixtures
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")