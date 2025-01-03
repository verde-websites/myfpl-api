from fastapi import HTTPException
from typing import List
from src import crud
from src.middleware import DB
from src.schemas.fixtures import Fixture, GetFixturesResponse

async def get_fixtures(db: DB, gameweek_id: int) -> GetFixturesResponse:
    """
    Retrieve fixtures by gameweek ID and convert them into Pydantic models.

    - **gameweek_id**: ID of the gameweek
    """
    fixtures_query = await crud.get_fixtures_by_gameweek_id(db, gameweek_id)
    
    if not fixtures_query:
        raise HTTPException(status_code=404, detail="Fixtures not found")
    
    # Convert each SQLAlchemy ORM instance to a Pydantic Fixture model
    fixtures_pydantic: List[Fixture] = [Fixture.model_validate(fixture) for fixture in fixtures_query]
    
    # Wrap the list of Fixture models into the GetFixturesResponse model
    return GetFixturesResponse(fixtures=fixtures_pydantic)