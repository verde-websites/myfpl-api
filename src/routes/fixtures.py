from src import services
from src.middleware import DB

async def get_fixtures(db: DB, gameweek_id: int):
    """
    Get the fixtures
    - **gameweek_id**: ID of the gameweek
    """
    return await services.get_fixtures(db, gameweek_id)