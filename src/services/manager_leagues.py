import json
from curl_cffi import CurlError, requests 

from src.schemas.fpl.entry import EntryFPLResponse
from src.schemas.manager import ClassicLeague, GetManagerLeagueResponse, H2HLeague
from fastapi import HTTPException

async def get_manager_leagues(manager_id: int):
    """
    Get the manager leagues.
    - **manager_id**: ID of the manager
    """
    base_url = "https://fantasy.premierleague.com/api"
    endpoint = f"{base_url}/entry/{manager_id}/"

    try:
        session = requests.Session()
        response = session.get(endpoint, timeout=10.0)
        response.raise_for_status()  # Raises HTTPError for bad responses

        try:
            data = response.json()
            leagues_data = EntryFPLResponse(**data)
            leagues = leagues_data.leagues

            # Transform back into dict to pass into another Pydantic Model and validate classic leagues - not sure if this is the best way to do it
            classic_leagues = [
                ClassicLeague(**league.model_dump()) for league in leagues.classic
            ]

            # Transform and validate head-to-head leagues
            h2h_leagues = [
                H2HLeague(**league.model_dump()) for league in leagues.h2h
            ]

            # Package the transformed data into the response model
            return GetManagerLeagueResponse(
                classic=classic_leagues,
                h2h=h2h_leagues
            )
      
        except json.JSONDecodeError as json_err:
            raise HTTPException(status_code=500, detail=f"Error decoding JSON: {json_err}")
        except Exception as parse_err:
            raise HTTPException(status_code=500, detail=f"Error parsing leagues data: {parse_err}")
        
    except CurlError as req_err:
        raise HTTPException(status_code=500, detail=f"Request to FPL API failed: {req_err}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
