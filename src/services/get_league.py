import json
from typing import Optional
from curl_cffi import CurlError, requests 

from src.schemas.leagues import LeagueMetadata, GetLeagueResponse, Standings
from src.schemas.fpl.classic_league_standings import ClassicLeagueStandingsResponse
from fastapi import HTTPException

async def get_classic_league(league_id: int, page: Optional[int] = None):
    """
    Get the league.
    - **league_id**: ID of the league
    - **page**: (Optional) Page number for pagination
    """
    base_url = "https://fantasy.premierleague.com/api"
    endpoint = f"{base_url}/leagues-classic/{league_id}/standings/"

    if page:
        endpoint += f"?page_standings={page}"

    try:
        session = requests.Session()
        response = session.get(endpoint, timeout=10.0)
        response.raise_for_status()  # Raises HTTPError for bad responses

        try:
            data = response.json()
            classic_league_data = ClassicLeagueStandingsResponse(**data)

            metadata = LeagueMetadata(**classic_league_data.league.model_dump())

            standings = Standings(**classic_league_data.standings.model_dump())

            # Package the transformed data into the response model
            return GetLeagueResponse(
                metadata=metadata,
                standings=standings
            )
      
        except json.JSONDecodeError as json_err:
            raise HTTPException(status_code=500, detail=f"Error decoding JSON: {json_err}")
        except Exception as parse_err:
            raise HTTPException(status_code=500, detail=f"Error parsing leagues data: {parse_err}")
        
    except CurlError as req_err:
        raise HTTPException(status_code=500, detail=f"Request to FPL API failed: {req_err}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
