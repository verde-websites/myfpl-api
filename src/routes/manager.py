from http.client import HTTPException
from ..middleware import DB
from .. import crud
from ..controllers import manager as manager_controller

async def get_manager(db: DB, manager_id: int):
    """
    Get the manager
    """
    # populate gameweek
    gameweek = await crud.get_current_gameweek(db)

    # Call Controller Method with Gameweek id and Manager ID 
    manager = await manager_controller.get_manager(gameweek.id, manager_id)

    return manager

