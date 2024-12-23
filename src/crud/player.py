import pprint
from typing import List
from src.models import Player as PlayerDBModel, PlayerFixture as PlayerFixtureDBModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_players(db: AsyncSession, players: List[int]):
    """
    Get the players from the database
    """

    players_query = await db.execute(select(PlayerDBModel).where(PlayerDBModel.fpl_tracker_id.in_(players)))
    players_list = players_query.scalars().all()
    return players_list


async def get_player_fixtures(db: AsyncSession, gameweek_id: int, players: List[int]):
    """
    Get the player fixtures from the database
    """
    pprint.pprint(players)
    player_fixtures_query = await db.execute(
        select(PlayerFixtureDBModel).where(
            PlayerFixtureDBModel.player_fpl_tracker_id.in_(players),
            PlayerFixtureDBModel.game_week_id == gameweek_id
        )
    )
    player_fixtures_list = player_fixtures_query.scalars().all()
    pprint.pprint(player_fixtures_list)
    return player_fixtures_list
