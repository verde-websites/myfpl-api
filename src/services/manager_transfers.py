import httpx

from src import crud
from ..middleware import DB
from fastapi import HTTPException


async def get_manager_transfers(db: DB, manager_id: int, gameweek_id: int):
    """
    Get the manager transfers for a specific gameweek.
    """
    base_url = "https://fantasy.premierleague.com/api/entry/"
    endpoint = f"{base_url}{manager_id}/transfers/"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(endpoint, timeout=10.0)
            transfers_data = response.json()

            gameweek_transfers = [
                transfer for transfer in transfers_data
                if transfer.get("event") == gameweek_id
            ]

            transfer_count = len(gameweek_transfers)

            gameweek_transfer_elements = [
                {
                    "player_in_id": transfer.get("element_in"),
                    "player_in_cost": transfer.get("element_in_cost"),
                    "player_out_id": transfer.get("element_out"),
                    "player_out_cost": transfer.get("element_out_cost")
                }
                for transfer in gameweek_transfers
            ]

            player_ids = set()
            for transfer in gameweek_transfer_elements:
                player_ids.add(transfer["player_in_id"])
                player_ids.add(transfer["player_out_id"])

            transfer_players_data = await crud.get_players(db, list(player_ids))

            player_id_to_details = {
                player.fpl_tracker_id: {
                    "first_name": player.first_name,
                    "second_name": player.second_name,
                    "web_name": player.web_name
                }
                for player in transfer_players_data
            }

            transfer_details = []

            for transfer in gameweek_transfer_elements:
                player_in = player_id_to_details.get(transfer["player_in_id"], {})
                player_out = player_id_to_details.get(transfer["player_out_id"], {})

                transfer["player_in_first_name"] = player_in.get("first_name", "Unknown")
                transfer["player_in_second_name"] = player_in.get("second_name", "Unknown")
                transfer["player_in_web_name"] = player_in.get("web_name", "Unknown")
                transfer["player_out_first_name"] = player_out.get("first_name", "Unknown")
                transfer["player_out_second_name"] = player_out.get("second_name", "Unknown")
                transfer["player_out_web_name"] = player_out.get("web_name", "Unknown")
                transfer_info = {
                    "player_in": {
                        "player_in_id": transfer["player_in_id"],
                        "player_in_cost": transfer["player_in_cost"],
                        "player_in_first_name": transfer["player_in_first_name"],
                        "player_in_second_name": transfer["player_in_second_name"],
                        "player_in_web_name": transfer["player_in_web_name"],
                    },
                    "player_out": {
                        "player_out_id": transfer["player_out_id"],
                        "player_out_cost": transfer["player_out_cost"],
                        "player_out_first_name": transfer["player_out_first_name"],
                        "player_out_second_name": transfer["player_out_second_name"],
                        "player_out_web_name": transfer["player_out_web_name"],
                    }
                }
                transfer_details.append(transfer_info)

            return {
                "transfer_count": transfer_count,
                "details": transfer_details
            }






            return transfer_data
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Request to FPL API failed: {e}")
        except httpx.TimeoutException:
            raise HTTPException(status_code=500, detail="Request to FPL API timed out")
