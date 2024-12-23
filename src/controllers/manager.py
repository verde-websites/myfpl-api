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

            # Get all transfers that occurred in the current gameweek
            gameweek_transfers = [
                transfer for transfer in transfers_data
                if transfer.get("event") == gameweek_id
            ]

            # Get the number of transfers that occurred in the current gameweek
            transfer_count = len(gameweek_transfers)

            # Loop through this gameweek's transfers and get the player IDs and costs
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
            transfer_players_data = await crud.get_players(db, list(player_ids))

            # Loop through players from the query and create a mapping from player ID to player details
            player_id_to_details = {
                player.fpl_tracker_id: {
                    "first_name": player.first_name,
                    "second_name": player.second_name,
                    "web_name": player.web_name
                }
                for player in transfer_players_data
            }

            transfer_details = []
            # Integrate player names into transfer elements and format for response
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

            # Grab all player IDs from picks object for the gameweek and query the database for live data
            player_ids = [pick["element"] for pick in picks_data["picks"]]

            # Query Live Data from Database
            live_players_data = await crud.get_player_fixtures(db, gameweek_id, player_ids)
            # Query Static Data from Database
            static_players_data = await crud.get_players(db, player_ids)

            # Combine Live and Static Data
            # Create a mapping for static data keyed by 'fpl_tracker_id'
            static_players_dict = {player.fpl_tracker_id: player for player in static_players_data}
            element_to_pick = {pick["element"]: pick for pick in picks_data["picks"]}

            combined_players_data = []
            for live_player in live_players_data:
                matching_pick = element_to_pick.get(live_player.player_fpl_tracker_id)

                # Assuming 'player_fpl_tracker_id' corresponds to 'fpl_tracker_id'
                static_player = static_players_dict.get(live_player.player_fpl_tracker_id)
                if static_player:
                    combined_player = {
                        "fpl_tracker_id": static_player.fpl_tracker_id,
                        "first_name": static_player.first_name,
                        "second_name": static_player.second_name,
                        "web_name": static_player.web_name,
                        "position": static_player.player_type,
                        "price": static_player.price,
                        "status": static_player.status,
                        "minutes": live_player.minutes,
                        "total_points": live_player.total_points,
                        "assists": live_player.assists,
                        "goals_scored": live_player.goals_scored,
                        "own_goals": live_player.own_goals,
                        "yellow_cards": live_player.yellow_cards,
                        "red_cards": live_player.red_cards,
                        "bps_points": live_player.bps_points,
                        "team_id": live_player.team_id,
                        "is_captain": matching_pick.get("is_captain", False),
                        "is_vice_captain": matching_pick.get("is_vice_captain", False),
                        "multiplier": matching_pick.get("multiplier", 1),
                        "team_position": matching_pick.get("position", 0)
                    }
                    combined_players_data.append(combined_player)
                else:
                    # Handle cases where static data is missing
                    combined_player = {
                        "fpl_tracker_id": live_player.player_fpl_tracker_id,
                        "first_name": "Unknown",
                        "second_name": "Unknown",
                        "web_name": "Unknown",
                        "minutes": live_player.minutes,
                        "total_points": live_player.total_points,
                        "assists": live_player.assists,
                        "goals_scored": live_player.goals_scored,
                        "own_goals": live_player.own_goals,
                        "yellow_cards": live_player.yellow_cards,
                        "red_cards": live_player.red_cards,
                        "bps_points": live_player.bps_points,
                        "team_id": live_player.team_id,
                    }                   
                    combined_players_data.append(combined_player)

            return {
                "metadata": metadata,
                "transfers": {
                    "number_of_transfers": transfer_count,
                    "details": transfer_details
                },
                "players": combined_players_data,
            }

        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while requesting data: {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
