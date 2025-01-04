from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from src.models import Fixture as FixtureDBModel
from src.models import Team as TeamDBModel
from src.models import PlayerFixture as PlayerFixtureDBModel

async def get_fixtures_by_gameweek_id(db: AsyncSession, gameweek_id: int):
    fixtures_query = await db.execute(select(FixtureDBModel).where(FixtureDBModel.game_week_id == gameweek_id))
    fixtures_list = fixtures_query.scalars().all()
    return fixtures_list

async def get_teams_by_ids(db: AsyncSession, team_ids: list[int]):
    teams_query = await db.execute(select(TeamDBModel).where(TeamDBModel.id.in_(team_ids)))
    teams_list = teams_query.scalars().all()
    return teams_list

async def get_red_cards_count_by_fixture_and_team(db: AsyncSession, fixture_ids: list[int]):
    """
    Retrieve the count of red card entries from the player_fixtures table
    based on fixture_ids, grouped by fixture_id and team_id.
    """
    red_cards_query = await db.execute(
        select(
            PlayerFixtureDBModel.fixture_id,
            PlayerFixtureDBModel.team_id,
            func.count(PlayerFixtureDBModel.id).label('red_card_count')
        )
        .where(
            PlayerFixtureDBModel.fixture_id.in_(fixture_ids),
            PlayerFixtureDBModel.red_cards == True
        )
        .group_by(
            PlayerFixtureDBModel.fixture_id,
            PlayerFixtureDBModel.team_id
        )
    )
    red_cards = red_cards_query.all()
    return red_cards