from http.client import HTTPException
from src import crud
from src.middleware import DB

async def get_fixtures(db: DB, gameweek_id: int):
    """
    Get the fixture
    - **gameweek_id**: ID of the gameweek
    """
    fixtures_query = await crud.get_fixtures_by_gameweek_id(db, gameweek_id)
    if not fixtures_query:
        raise HTTPException(status_code=404, detail="Fixtures not found")
    return fixtures_query