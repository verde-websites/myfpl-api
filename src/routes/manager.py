from http.client import HTTPException

from src import services
from ..middleware import DB
from .. import crud
import httpx
from fastapi import HTTPException

async def get_manager(db: DB, manager_id: int):
    """
    Get the manager
    """

    # now THIS is what I call validation
    if manager_id <= 0:
        raise HTTPException(status_code=422, detail="Invalid manager_id")

    gameweek = await crud.get_current_gameweek(db)
    if not gameweek:
        raise HTTPException(status_code=404, detail="No current gameweek found")

    try:
        metadata = await services.get_manager_metadata(manager_id, gameweek.id)
        transfers_data = await services.get_manager_transfers_by_gameweek(db, manager_id, gameweek.id)
        live_players_data = await services.get_live_players_by_gameweek(db, manager_id, gameweek.id)

        if not metadata:
            raise HTTPException(status_code=404, detail="Unable to retrieve manager's metadata for this gameweek.")
        if not transfers_data:
            raise HTTPException(status_code=404, detail="Unable to retrieve manager's transfers for this gameweek.")
        if not live_players_data:
            raise HTTPException(status_code=404, detail="Unable to retrieve manager's live players for this gameweek.")

        return {
            "metadata": metadata,
            "transfers": transfers_data,
            "players": live_players_data,
        }

    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while requesting data: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")