import httpx
from fastapi import HTTPException
import asyncio

async def get_manager(gameweek_id: int, manager_id: int):
    """
    Get the manager along with transfers and picks for a specific gameweek.
    """
    base_url = "https://fantasy.premierleague.com/api/entry/"
    endpoints = {
        "manager": f"{base_url}{manager_id}/",
        "transfers": f"{base_url}{manager_id}/transfers/",
        "picks": f"{base_url}{manager_id}/event/{gameweek_id}/picks/"
    }

    async with httpx.AsyncClient() as client:
        try:
            tasks = [client.get(url, timeout=10.0) for url in endpoints.values()]
            responses = await asyncio.gather(*tasks)

            # Endpoint Data Objects
            manager_data = responses[0].json()
            transfers_data = responses[1].json()
            picks_data = responses[2].json()

            # Reformatting Data for Response
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

            transfers = [
                transfer for transfer in transfers_data
                if transfer.get("event") == gameweek_id
            ]

            # Grab all player IDs from picks object for the gameweek
            players = [pick["element"] for pick in picks_data["picks"]]
            # Query the Database using the player IDs for live data
            # players_data = await get_players(players)

            return {
                "metadata": metadata,
                "transfers": transfers,
                "players": players
            }


        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while requesting data: {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
