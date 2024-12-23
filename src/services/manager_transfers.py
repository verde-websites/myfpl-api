async def get_manager_transfers(db: DB, manager_id: int, gameweek_id: int):
    """
    Get the manager transfers for a specific gameweek.
    """
    base_url = "https://fantasy.premierleague.com/api/entry/"
    endpoint = f"{base_url}{manager_id}/transfers/"
