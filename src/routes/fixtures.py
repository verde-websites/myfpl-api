from src.middleware import DB


async def get_fixture(db: DB, gameweek_id: int):
    """
    Get the fixture
    - **gameweek_id**: ID of the gameweek
    """
    # return await services.get_fixture(db, gameweek_id)