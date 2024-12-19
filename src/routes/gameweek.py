from http.client import HTTPException
from ..middleware import DB
from .. import crud

async def get_current_gameweek(db: DB):
    """
    Get the current gameweek
    """
    current_gameweek = await crud.get_current_gameweek(db)
    if not current_gameweek:
        raise HTTPException(status_code=404, detail="Current gameweek not found")
    return current_gameweek
