import httpx
import json
from fastapi import HTTPException
from ..middleware import DB
from .. import crud

async def get_live_players_by_gameweek(db: DB, manager_id: int, gameweek_id: int):
    """
    Get the live players for a specific gameweek.
    """
    base_url = "https://fantasy.premierleague.com/api/entry/"
    endpoint = f"{base_url}{manager_id}/event/{gameweek_id}/picks/"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(endpoint, timeout=10.0)
            response.raise_for_status()  # Raises HTTPError for bad responses

            try:
                picks_data = response.json()
            except json.JSONDecodeError as json_err:
                # Log the response content for debugging
                error_content = response.text
                raise HTTPException(
                    status_code=500,
                    detail=f"JSON decoding failed: {json_err}. Response content: {error_content}"
                )

            # Proceed with processing picks_data as before
            player_ids = [pick["element"] for pick in picks_data.get("picks", [])]

            # Query Live Data from Database
            live_players_data = await crud.get_player_fixtures(db, gameweek_id, player_ids)
            # Query Static Data from Database
            static_players_data = await crud.get_players(db, player_ids)

            # Combine Live and Static Data
            static_players_dict = {player.fpl_tracker_id: player for player in static_players_data}
            element_to_pick = {pick["element"]: pick for pick in picks_data.get("picks", [])}

            combined_players_data = []
            for live_player in live_players_data:
                matching_pick = element_to_pick.get(live_player.player_fpl_tracker_id)
                static_player = static_players_dict.get(live_player.player_fpl_tracker_id)
                
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
                    "is_captain": matching_pick.get("is_captain", False) if matching_pick else False,
                    "is_vice_captain": matching_pick.get("is_vice_captain", False) if matching_pick else False,
                    "multiplier": matching_pick.get("multiplier", 1) if matching_pick else 1,
                    "team_position": matching_pick.get("position", 0) if matching_pick else 0
                }
                combined_players_data.append(combined_player)
                

            return combined_players_data

        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Request to FPL API failed: {e}")
    