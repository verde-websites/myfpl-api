import json
from fastapi import HTTPException
from curl_cffi import requests, CurlError
from src.schemas.fpl.entry import EntryFPLResponse
from src.schemas.fpl.picks import PicksFPLResponse

async def get_manager_metadata(manager_id: int, gameweek_id: int):
    """
    Get the manager metadata for a specific gameweek.
    """
    base_url = "https://fantasy.premierleague.com/api/entry/"
    endpoints = {
        "manager": f"{base_url}{manager_id}/",
        "picks": f"{base_url}{manager_id}/event/{gameweek_id}/picks/"
    }

    try:
        session = requests.Session()
        
        # Fetch manager data
        response_manager = session.get(endpoints["manager"], timeout=10.0)
        response_manager.raise_for_status()
        
        # Fetch picks data
        response_picks = session.get(endpoints["picks"], timeout=10.0)
        response_picks.raise_for_status()

        try:
            manager_json = response_manager.json()
            picks_json = response_picks.json()
            manager_data = EntryFPLResponse(**manager_json)
            picks_data = PicksFPLResponse(**picks_json)
        except json.JSONDecodeError as json_err:
            # Log the response content for debugging
            error_content_manager = response_manager.text
            error_content_picks = response_picks.text

            raise HTTPException(
                status_code=500,
                detail=(
                    f"JSON decoding failed: {json_err}. "
                    f"Manager response content: {error_content_manager}. "
                    f"Picks response content: {error_content_picks}."
                )
            )

        first_name = manager_data.player_first_name
        last_name = manager_data.player_last_name
        manager_name = f"{first_name} {last_name}".strip()

        metadata = {
            "id": manager_data.id,
            "manager_name": manager_name,
            "team_name": manager_data.team_name,
            "gameweek_rank": picks_data.entry_history.gameweek_rank,
            "overall_rank": picks_data.entry_history.overall_rank,
            "points": picks_data.entry_history.points,
            "total_points": picks_data.entry_history.total_points,
            "team_value": picks_data.entry_history.team_value,
            "points_on_bench": picks_data.entry_history.points_on_bench,
            "bank": picks_data.entry_history.bank,
            "percentile_rank": picks_data.entry_history.percentile_rank
        }

        return metadata

    except CurlError as e:
        raise HTTPException(status_code=500, detail=f"Error fetching manager metadata: {str(e)}")