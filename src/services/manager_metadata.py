import json
import httpx
import asyncio
from fastapi import HTTPException

async def get_manager_metadata(manager_id: int, gameweek_id: int):
    """
    Get the manager metadata for a specific gameweek.
    """
    base_url = "https://fantasy.premierleague.com/api/entry/"
    endpoints = {
        "manager": f"{base_url}{manager_id}/",
        "picks": f"{base_url}{manager_id}/event/{gameweek_id}/picks/"
    }

    async with httpx.AsyncClient() as client:
        try:
            tasks = [client.get(url, timeout=10.0) for url in endpoints.values()]
            responses = await asyncio.gather(*tasks)
            responses[0].raise_for_status()  # Raises HTTPError for bad responses
            responses[1].raise_for_status()  # Raises HTTPError for bad responses

            try:
                manager_data = responses[0].json()
                picks_data = responses[1].json()
            except json.JSONDecodeError as json_err:
                # Log the response content for debugging
                error_content_manager = responses[0].text
                error_content_picks = responses[1].text

                raise HTTPException(
                    status_code=500,
                   detail=(
                        f"JSON decoding failed: {json_err}. "
                        f"Manager response content: {error_content_manager}. "
                        f"Picks response content: {error_content_picks}."
                    )
                )

            first_name = manager_data.get("player_first_name", "")
            last_name = manager_data.get("player_last_name", "")
            manager_name = f"{first_name} {last_name}".strip()

            metadata = {
                "id": manager_data.get("id"),
                "manager_name": manager_name,
                "team_name": manager_data.get("name"),
                "gameweek_rank": picks_data["entry_history"]["rank"],
                "overall_rank": picks_data["entry_history"]["overall_rank"],
                "points": picks_data["entry_history"]["points"],
                "total_points": picks_data["entry_history"]["total_points"],
                "team_value": picks_data["entry_history"]["value"],
                "points_on_bench": picks_data["entry_history"]["points_on_bench"],
                "bank": picks_data["entry_history"]["bank"],
                "percentile_rank": picks_data["entry_history"]["percentile_rank"]
            }

            return metadata
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching manager metadata: {str(e)}")