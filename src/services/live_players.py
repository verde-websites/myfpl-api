import httpx
from fastapi import HTTPException
from ..middleware import DB
from .. import crud

async def get_live_players_by_gameweek(db: DB, manager_id: int, gameweek_id: int):
    """
    Get the live players for a specific gameweek.
    """
    base_url = "https://fantasy.premierleague.com/api/fixtures/"
    endpoint = f"{base_url}{manager_id}/event/{gameweek_id}/picks/"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(endpoint, timeout=10.0)
            picks_data = response.json()

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

            return combined_players_data
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Request to FPL API failed: {e}")
    