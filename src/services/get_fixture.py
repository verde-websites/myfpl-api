from src.middleware import DB

async def get_fixture(db: DB, gameweek_id: int):
    """
    Get the fixture
    - **gameweek_id**: ID of the gameweek
    """
    # return await db.execute_query("SELECT * FROM fixtures WHERE gameweek_id = %s", (gameweek_id,))