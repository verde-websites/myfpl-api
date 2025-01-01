import json
from fastapi import HTTPException

from src.schemas.fpl.picks import PicksFPLResponse
from ..middleware import DB
from .. import crud
import logging
from curl_cffi import CurlError, requests 

logger = logging.getLogger(__name__)


async def get_live_players_by_gameweek(db: DB, manager_id: int, gameweek_id: int):
    """
    Get the live players for a specific gameweek.
    """
    base_url = "https://fantasy.premierleague.com/api/entry/"
    endpoint = f"{base_url}{manager_id}/event/{gameweek_id}/picks/"

    try:
        session = requests.Session()
        response = session.get(endpoint, timeout=10.0)
        response.raise_for_status()  # Raises HTTPError for bad responses

        try:
            data = response.json()
            picks_data = PicksFPLResponse(**data)
        except json.JSONDecodeError as json_err:
            # Log the response content for debugging
            error_content = response.text
            raise HTTPException(
                status_code=500,
                detail=f"JSON decoding failed: {json_err}. Response content: {error_content}"
            )

        # Proceed with processing picks_data as before
        player_ids = [pick.fpl_tracker_id for pick in picks_data.picks]

        # Query Live Data from Database
        live_players_data = await crud.get_player_fixtures(db, gameweek_id, player_ids)
        if not live_players_data:
            logger.error("Player Fixture Query Failed. Gameweek updating or problem with current gameweeks data.")
        # Query Static Data from Database
        static_players_data = await crud.get_players(db, player_ids)
        if not static_players_data:
            logger.error("Get Players Query Failed")

        # Combine Live and Static Data
        static_players_dict = {player.fpl_tracker_id: player for player in static_players_data}
        element_to_pick = {pick.fpl_tracker_id: pick for pick in picks_data.picks}

        combined_players_data = []
        for live_player in live_players_data:
            matching_pick = element_to_pick.get(live_player.player_fpl_tracker_id)
            static_player = static_players_dict.get(live_player.player_fpl_tracker_id)
            
            # Check Input type validation before calculation- probably should be done for everything that we return, but yeah cba.
            if not isinstance(live_player.total_points, int):
                logger.error(f"Invalid 'total_points': Expected int, got {type(live_player.total_points).__name__}")
                raise HTTPException(
                    status_code=500,
                    detail="Invalid data format from FPL API: 'total_points' must be an integer."
                )

            multiplier = matching_pick.multiplier
            if not isinstance(multiplier, int):
                raise HTTPException(
                    status_code=500,
                    detail=f"Invalid data format from FPL API: 'multiplier' must be an integer, got {type(multiplier).__name__}."
                )
            
            combined_player = {
                "fpl_tracker_id": static_player.fpl_tracker_id,
                "first_name": static_player.first_name,
                "second_name": static_player.second_name,
                "web_name": static_player.web_name,
                "position": static_player.player_type,
                "price": static_player.price,
                "status": static_player.status,
                "minutes": live_player.minutes,
                "points": live_player.total_points,
                "assists": live_player.assists,
                "goals_scored": live_player.goals_scored,
                "own_goals": live_player.own_goals,
                "yellow_cards": live_player.yellow_cards,
                "red_cards": live_player.red_cards,
                "bps_points": live_player.bps_points,
                "team_id": live_player.team_id,
                "is_captain": matching_pick.is_captain if matching_pick else False,
                "is_vice_captain": matching_pick.is_vice_captain if matching_pick else False,
                "multiplier": matching_pick.multiplier if matching_pick else 1,
                "team_order": matching_pick.team_order if matching_pick else 0
            }
            combined_players_data.append(combined_player)
            

        return combined_players_data

    except CurlError as e:
        logger.error(f"Request to FPL API failed: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error.")    