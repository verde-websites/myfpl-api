import json
from curl_cffi import CurlError, requests 

# from src.schemas.leagues import LeagueMetadata, GetLeagueResponse
from src.schemas.fpl.classic_league_standings import ClassicLeagueStandingsResponse, Entry
from fastapi import HTTPException

async def get_league(league_id: int):
    """
    Get the league.
    - **league_id**: ID of the league
    """
    base_url = "https://fantasy.premierleague.com/api"
    endpoint = f"{base_url}/leagues-classic/{league_id}/standings/"

    try:
        session = requests.Session()
        response = session.get(endpoint, timeout=10.0)
        response.raise_for_status()  # Raises HTTPError for bad responses

        try:
            data = response.json()
            classic_league_data = ClassicLeagueStandingsResponse(**data)

            metadata = LeagueMetadata(**classic_league_data.league)

            standings = [
                Entry(**entry.model_dump()) for entry in classic_league_data.standings.results
            ]

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
