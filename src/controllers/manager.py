import pprint
import httpx
from fastapi import HTTPException
import asyncio
from .. import crud
from ..middleware import DB

async def get_manager(db: DB, gameweek_id: int, manager_id: int):
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

            # Get all transfers that occured in the current gameweek
            gameweek_transfers = [
                transfer for transfer in transfers_data
                if transfer.get("event") == gameweek_id
            ]

            # Get the number of transfers that occured in the current gameweek
            transfer_count = len(gameweek_transfers)

            # Loop through this gameweeks transfers and get the player IDs and costs
            gameweek_transfer_elements = [
                {
                    "player_in_id": transfer.get("element_in"),
                    "player_in_cost": transfer.get("element_in_cost"),
                    "player_out_id": transfer.get("element_out"),
                    "player_out_cost": transfer.get("element_out_cost")
                }
                for transfer in gameweek_transfers
            ]

            # Extract unique player IDs for Database Query
            player_ids = set()
            for transfer in gameweek_transfer_elements:
                player_ids.add(transfer["player_in_id"])
                player_ids.add(transfer["player_out_id"])

            # Fetch player data from the database
            players_data = await crud.get_players(db, list(player_ids))

            # Loop through players from the query and create a mapping from player ID to player details
            player_id_to_details = {
                player.fpl_tracker_id: {
                    "web_name": player.web_name
                }
                for player in players_data
            }

            transfer_details = []
            # Integrate player names into transfer elements and format for response
            for transfer in gameweek_transfer_elements:
                player_in = player_id_to_details.get(transfer["player_in_id"], {})
                player_out = player_id_to_details.get(transfer["player_out_id"], {})
                
                transfer["player_in_web_name"] = player_in.get("web_name", "Unknown")
                transfer["player_out_web_name"] = player_out.get("web_name", "Unknown")
                transfer_info = {
                    "player_in": {
                        "player_in_id": transfer["player_in_id"],
                        "player_in_cost": transfer["player_in_cost"],
                        "player_in_web_name": transfer["player_in_web_name"],
                    },
                    "player_out": {
                        "player_out_id": transfer["player_out_id"],
                        "player_out_cost": transfer["player_out_cost"],
                        "player_out_web_name": transfer["player_out_web_name"],
                    }
                }
                transfer_details.append(transfer_info)

            # Grab all player IDs from picks object for the gameweek
            players = [pick["element"] for pick in picks_data["picks"]]
            # TODO: Query the Database using the player IDs for live data
            # players_data = await get_players(players)

            return {
                "metadata": metadata,
                "transfers": {
                    "number_of_transfers": transfer_count,
                    "details": transfer_details
                },
                "players": players,
            }


        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while requesting data: {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
