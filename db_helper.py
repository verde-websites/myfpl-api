import asyncio
import pandas as pd
import requests
from sqlalchemy import insert, text
from git import Repo
import yaml
from src.schemas.fpl import BootstrapStaticFPLResponse,BootstrapStaticPlayersResponse, BootstrapStaticGameweeksResponse, BootstrapStaticTeamsResponse, FixturesFPLResponse
import os
from src.database import SessionLocal
from src.models import Season as SeasonDBModel
from src.models import Gameweek as GameWeekDBModel
from src.models import Team as TeamDBModel
from src.models import Fixture as FixtureDBModel
from src.models import Player as PlayerDBModel
from src.models import TeamFplSeason as TeamFPLSeasonDBModel
from src.models import PlayerFplSeason as PlayerFPLSeasonDBModel
from src.models import PlayerFixture as PlayerFixtureDBModel
import argparse

def get_bootstrap_static_data():
    # Get data from bootstrap-static endpoint
    response = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/")
    bootstrap_static_data = BootstrapStaticFPLResponse(**response.json())
    return bootstrap_static_data

def get_fixtures_data():
    # Get data from fixtures endpoint
    response = requests.get(f"https://fantasy.premierleague.com/api/fixtures")
    data = response.json()
    # delete the first item
    data.pop(0)
    fixtures_data = FixturesFPLResponse(fixtures=data)
    return fixtures_data

def create_gameweeks_fixture_files(bootstrap_gameweeks_data: BootstrapStaticGameweeksResponse):
    print(f'Creating gameweek database fixtures')
    gameweek_fixtures = []
    for gameweek in bootstrap_gameweeks_data:
        gameweek_fixture_entry = {
            "id": gameweek.id,
            "gameweek_number": gameweek.id,
            "name": gameweek.name,
            "transfer_deadline": gameweek.deadline_time,
            "gameweek_active": gameweek.is_current,
            "gameweek_finished": gameweek.finished,
            "data_checked": gameweek.data_checked
        }
        gameweek_fixtures.append(gameweek_fixture_entry)
    with open('fixtures/gameweeks.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(gameweek_fixtures, f, sort_keys=False, default_flow_style=False, allow_unicode=True)
    return gameweek_fixtures

def create_teams_fixture_files(bootstrap_teams_data: BootstrapStaticTeamsResponse):
    print(f'Creating team database fixtures')
    team_fixtures = {}
    for team in bootstrap_teams_data:
        team_fixture_entry = {
            "id": team.code,
            "fpl_tracker_id": team.id,
            "team_name": team.name,
            "short_name": team.short_name
        }
        team_fixtures[team.id] = team_fixture_entry
    team_fixtures_list = list(team_fixtures.values())
    with open('fixtures/teams.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(team_fixtures_list, f, sort_keys=False, default_flow_style=False, allow_unicode=True)
    return team_fixtures_list, team_fixtures

def create_team_fpl_seasons_fixture_files(team_fixtures: list):
    print(f'Creating team_fpl_season database fixtures')
    team_fpl_seasons_fixtures = []
    for team in team_fixtures:
        team_fpl_seasons_fixture_entry = {
            "team_id": team["id"],
            "season_id": 2
        }
        team_fpl_seasons_fixtures.append(team_fpl_seasons_fixture_entry)
    with open('fixtures/team_fpl_seasons.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(team_fpl_seasons_fixtures, f, sort_keys=False, default_flow_style=False, allow_unicode=True)
    return team_fpl_seasons_fixtures

def create_players_fixture_files(bootstrap_players_data: BootstrapStaticPlayersResponse):
    print(f'Creating player database fixtures')
    player_fixtures = []
    for player in bootstrap_players_data:
        player_fixture_entry = {
            "id": player.code,
            "fpl_tracker_id": player.id,
            "first_name": player.first_name,
            "second_name": player.second_name,
            "web_name": player.web_name,
            "team_id": player.team_code,
            "status": player.status,
            "player_type": player.element_type,
            "price": player.now_cost,
            "form": player.form
        }
        player_fixtures.append(player_fixture_entry)
    with open('fixtures/players.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(player_fixtures, f, sort_keys=False, default_flow_style=False, allow_unicode=True)
    return player_fixtures

def create_player_fpl_seasons_fixture_files(player_fixtures: list):
    print(f'Creating player_fpl_season database fixtures')
    player_fpl_seasons_fixtures = []
    for player in player_fixtures:
        player_fpl_seasons_fixture_entry = {
            "player_id": player["id"],
            "season_id": 2
        }
        player_fpl_seasons_fixtures.append(player_fpl_seasons_fixture_entry)
    with open('fixtures/player_fpl_seasons.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(player_fpl_seasons_fixtures, f, sort_keys=False, default_flow_style=False, allow_unicode=True)
    return player_fpl_seasons_fixtures

def create_fixtures_fixture_files(fixtures_data: FixturesFPLResponse, teams_dict: dict):
    print(f'Creating fixture database fixtures')
    fixtures_fixtures = []
    for fixture in fixtures_data.fixtures:
        fixture_entry = {
            "id": fixture.code,
            "fpl_tracker_id": fixture.id,
            "season_id": 2,
            "game_week_id": fixture.event,
            "home_team_id": teams_dict[fixture.team_h]["id"],
            "away_team_id": teams_dict[fixture.team_a]["id"],
            "kickoff_time": fixture.kickoff_time,
            "minutes": fixture.minutes,
            "finished": fixture.finished,
            "finished_provisional": fixture.finished_provisional,
            "provisional_start_time": fixture.provisional_start_time,
            "started": fixture.started,
            "home_team_score": fixture.team_h_score,
            "away_team_score": fixture.team_a_score
        }
        fixtures_fixtures.append(fixture_entry)
    with open('fixtures/fixtures.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(fixtures_fixtures, f, sort_keys=False, default_flow_style=False, allow_unicode=True)
    return fixtures_fixtures

def clone_vaastav_repo(repo_url: str, clone_to: str):
    if not os.path.exists("vaastav"):
        print(f"Cloning repository {repo_url} to {clone_to}")
        Repo.clone_from(repo_url, clone_to)
    else:
        print(f"Repository {clone_to} already exists, pulling latest changes")
        # pull the latest changes
        repo = Repo(clone_to)
        repo.remotes.origin.pull()


def create_player_fixture_db_entries(teams: list, players: list, fixtures: list):
    print(f'Creating player_fixture database fixtures')
    player_fixture_db_entries = []
    # loop through the teams list and create a dictionary with the key being the team name and the value being the team
    team_dict = {}
    for team in teams:
        team_dict[team["team_name"]] = team
    # go through the players list and create a dictionaries with the key being the concatentation fo the first and second name
    player_dict = {}
    for player in players:
        player_dict[f"{player['first_name']} {player['second_name']}"] = player
    # loop through the fixtures list and create a dictionary with the key being the fixture fpl_tracker_id
    fixtures_dict = {}
    for fixture in fixtures:
        fixtures_dict[fixture["fpl_tracker_id"]] = fixture
    # Read all gameweek CSV files from vaastav repo
    gw_dir = "vaastav/data/2024-25/gws"
    for filename in os.listdir(gw_dir):
        if filename.endswith(".csv") and filename.startswith("gw"):
            gw_df = pd.read_csv(os.path.join(gw_dir, filename))
            gw_count = int(filename.split("gw")[1].split(".")[0])
            print(f"Processing gameweek {gw_count} from {filename}")
            
            # Process each row in the gameweek file
            for _, row in gw_df.iterrows():
                player_fixture_entry = {
                    "player_id": player_dict[row["name"]]["id"],
                    "player_fpl_tracker_id": player_dict[row["name"]]["fpl_tracker_id"],
                    "fixture_id": fixtures_dict[row["fixture"]]["id"],
                    "game_week_id": gw_count,
                    "team_id": team_dict[row["team"]]["id"],
                    "minutes": row["minutes"],
                    "clean_sheet": row["clean_sheets"],
                    "goals_scored": row["goals_scored"],
                    "goals_conceded": row["goals_conceded"],
                    "assists": row["assists"],
                    "saves": row["saves"],
                    "own_goals": row["own_goals"],
                    "penalties_saved": row["penalties_saved"],
                    "penalties_missed": row["penalties_missed"],
                    "yellow_cards": row["yellow_cards"],
                    "red_cards": row["red_cards"],
                    "bonus_points": row["bonus"],
                    "bps_points": row["bps"],
                    "influence": row["influence"],
                    "creativity": row["creativity"],
                    "threat": row["threat"],
                    "ict_index": row["ict_index"],
                    "started": True,
                    "expected_goals": row["expected_goals"],
                    "expected_assists": row["expected_assists"],
                    "expected_goal_involvements": row["expected_goal_involvements"],
                    "expected_goals_conceded": row["expected_goals_conceded"],
                    "total_points": row["total_points"],
                }
                player_fixture_db_entries.append(player_fixture_entry)
    # Write fixtures to YAML file
    with open('fixtures/player_fixtures.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(player_fixture_db_entries, f, sort_keys=False, default_flow_style=False, allow_unicode=True)
        
    return player_fixture_db_entries

async def seed_seasons():
    # read the seasons.yaml file
    seasons = []
    with open('fixtures/seasons.yaml', 'r') as f:
        seasons = yaml.safe_load(f)
    async with SessionLocal.begin() as db:
        for season in seasons:
            await db.execute(insert(SeasonDBModel).values(season))

async def seed_gameweeks():
    # seed all the gameweeks in one
    gameweeks = []
    with open('fixtures/gameweeks.yaml', 'r') as f:
        gameweeks = yaml.safe_load(f)
    async with SessionLocal.begin() as db:
        await db.execute(insert(GameWeekDBModel).values(gameweeks))

async def seed_teams():
    teams = []
    with open('fixtures/teams.yaml', 'r') as f:
        teams = yaml.safe_load(f)
    async with SessionLocal.begin() as db:
        await db.execute(insert(TeamDBModel).values(teams))

async def seed_fixtures():
    fixtures = []
    with open('fixtures/fixtures.yaml', 'r') as f:
        fixtures = yaml.safe_load(f)
    async with SessionLocal.begin() as db:
        await db.execute(insert(FixtureDBModel).values(fixtures))

async def seed_players():
    players = []
    with open('fixtures/players.yaml', 'r') as f:
        players = yaml.safe_load(f)
    async with SessionLocal.begin() as db:
        await db.execute(insert(PlayerDBModel).values(players))

async def seed_team_fpl_seasons():
    team_fpl_seasons = []
    with open('fixtures/team_fpl_seasons.yaml', 'r') as f:
        team_fpl_seasons = yaml.safe_load(f)
    async with SessionLocal.begin() as db:
        await db.execute(insert(TeamFPLSeasonDBModel).values(team_fpl_seasons))

async def seed_player_fpl_seasons():
    player_fpl_seasons = []
    with open('fixtures/player_fpl_seasons.yaml', 'r') as f:
        player_fpl_seasons = yaml.safe_load(f)
    async with SessionLocal.begin() as db:
        await db.execute(insert(PlayerFPLSeasonDBModel).values(player_fpl_seasons))

async def seed_player_fixtures():
    player_fixtures = []
    with open('fixtures/player_fixtures.yaml', 'r') as f:
        player_fixtures = yaml.safe_load(f)
    
    batch_size = 900
    for i in range(0, len(player_fixtures), batch_size):
        batch = player_fixtures[i:i + batch_size]
        async with SessionLocal.begin() as db:
            await db.execute(insert(PlayerFixtureDBModel).values(batch))

async def seed_database():
    print("Seeding database")
    await seed_seasons()
    print("Seeded seasons")
    await seed_gameweeks()
    print("Seeded gameweeks")
    await seed_teams()
    print("Seeded teams")
    await seed_fixtures()
    print("Seeded fixtures")
    await seed_players()
    print("Seeded players")
    await seed_team_fpl_seasons()
    print("Seeded team_fpl_seasons")
    await seed_player_fpl_seasons()
    print("Seeded player_fpl_seasons")
    await seed_player_fixtures()
    print("Seeded player_fixtures")

async def truncate_database():
    async with SessionLocal.begin() as db:
        await db.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        await db.execute(text("TRUNCATE TABLE player_fixtures"))
        await db.execute(text("TRUNCATE TABLE player_fpl_seasons"))
        await db.execute(text("TRUNCATE TABLE team_fpl_seasons"))
        await db.execute(text("TRUNCATE TABLE fixtures"))
        await db.execute(text("TRUNCATE TABLE teams"))
        await db.execute(text("TRUNCATE TABLE players"))
        await db.execute(text("TRUNCATE TABLE game_weeks"))
        await db.execute(text("TRUNCATE TABLE seasons"))
        await db.execute(text("SET FOREIGN_KEY_CHECKS = 1"))

async def generate_fixtures():
    clone_vaastav_repo("https://github.com/vaastav/Fantasy-Premier-League.git", "vaastav")
    bootstrap_static_data = get_bootstrap_static_data()
    fixtures_data = get_fixtures_data()
    create_gameweeks_fixture_files(bootstrap_static_data.gameweeks)
    teams_fixtures, teams_dict = create_teams_fixture_files(bootstrap_static_data.teams)
    create_team_fpl_seasons_fixture_files(teams_fixtures)
    players_fixtures = create_players_fixture_files(bootstrap_static_data.players)
    create_player_fpl_seasons_fixture_files(players_fixtures)
    fixtures_fixtures = create_fixtures_fixture_files(fixtures_data, teams_dict)
    create_player_fixture_db_entries(teams_fixtures, players_fixtures, fixtures_fixtures)

async def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='FPL data seeder')
    parser.add_argument('-g', '--generate', action='store_true', help='Generate fixture files')
    parser.add_argument('-s', '--seed', action='store_true', help='Seed the database')
    parser.add_argument('-t', '--truncate', action='store_true', help='Truncate the database')
    args = parser.parse_args()

    # If no arguments provided, show help
    if not args.generate and not args.seed and not args.truncate:
        parser.print_help()
        return

    # Generate fixtures if -g flag is present
    if args.generate:
        await generate_fixtures()

    if args.truncate:
        await truncate_database()

    # Seed database if -s flag is present
    if args.seed:
        await truncate_database()
        await seed_database()

if __name__ == "__main__":
    asyncio.run(main())