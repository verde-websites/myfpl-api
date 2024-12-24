import httpx
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
            transfer_data = response.json()
            return transfer_data
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Request to FPL API failed: {e}")
        except httpx.TimeoutException:
            raise HTTPException(status_code=500, detail="Request to FPL API timed out")
