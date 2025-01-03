from fastapi import HTTPException
from typing import List
from src import crud
from src.middleware import DB
from src.schemas.fixtures import Fixture, GetFixturesResponse

async def get_fixtures(db: DB, gameweek_id: int) -> GetFixturesResponse:
    """
    Retrieve fixtures by gameweek ID, append team names, and convert them into Pydantic models.

    - **gameweek_id**: ID of the gameweek
    """
    fixtures_query = await crud.get_fixtures_by_gameweek_id(db, gameweek_id)
    if not fixtures_query:
        raise HTTPException(status_code=404, detail="Couldn't find fixtures for this gameweek")
    
    home_team_ids = {fixture.home_team_id for fixture in fixtures_query}
    away_team_ids = {fixture.away_team_id for fixture in fixtures_query}
    combined_team_ids = home_team_ids.union(away_team_ids)
    
    teams = await crud.get_teams_by_ids(db, list(combined_team_ids))
    
    # Create a mapping from team ID to team name
    team_id_to_name = {team.id: team.team_name for team in teams}
    
    # Add team names to each fixture
    for fixture in fixtures_query:
        fixture.home_team_name = team_id_to_name.get(fixture.home_team_id)
        fixture.away_team_name = team_id_to_name.get(fixture.away_team_id)
    
    # Convert each manipulated fixture to a Pydantic Fixture model
    fixtures_pydantic: List[Fixture] = [Fixture.model_validate(fixture) for fixture in fixtures_query]
    
    # Wrap the list of Fixture models into the GetFixturesResponse model
    return GetFixturesResponse(fixtures=fixtures_pydantic)